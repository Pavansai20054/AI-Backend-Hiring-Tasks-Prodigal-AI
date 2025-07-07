from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, Field, conint
from typing import Literal, List, Optional
from embed import embed_texts
from vector_store import VectorStore
from ingest import ingest_csv, ingest_pdf
import os
import tempfile
import threading
import pathlib

from transformers import pipeline
import torch

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="RAG Service",
    description="Retrieval-Augmented Generation API for Titanic/Wine datasets",
    version="1.3.0",
    docs_url="/docs",
    redoc_url=None
)

vector_store = None
current_dataset = "titanic"
EMBEDDING_DIM = 384
DATA_PATH = "data"

qa_pipeline = None
gen_pipeline = None

class ContextItem(BaseModel):
    text: str
    source: str = "dataset_schema"
    score: Optional[float] = None
    relevance: Optional[str] = Field(None, example="high")

class RagQueryRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=1,
        example="Explain Pclass in Titanic"
    )
    top_k: conint(ge=1, le=10) = Field(  #type: ignore
        3,
        description="Number of context items to return",
        example=3
    )

class RagQueryResponse(BaseModel):
    query: str
    contexts: List[ContextItem]
    synthesized_answer: str
    dataset: str
    context_count: int

class ContextSwitchRequest(BaseModel):
    dataset: Literal["titanic", "wine"] = Field(
        ...,
        example="wine",
        description="Dataset to switch context to"
    )

def titanic_context():
    return [
        "Survived: 0 = No, 1 = Yes. Indicates if the passenger survived.",
        "Pclass: Ticket class (1 = 1st, 2 = 2nd, 3 = 3rd).",
        "Sex: Gender of the passenger.",
        "Age: Age in years.",
        "Fare: Passenger fare.",
        "SibSp: # of siblings / spouses aboard the Titanic.",
        "Parch: # of parents / children aboard the Titanic.",
        "Cabin: Cabin number.",
        "Embarked: Port of Embarkation (C = Cherbourg; Q = Queenstown; S = Southampton).",
        "The Titanic dataset contains information about passengers, including whether they survived, their age, sex, ticket class, and more.",
        "Most females survived, while most males did not.",
        "Children had a higher survival rate than adults."
    ]

def wine_context():
    return [
        "fixed acidity: most acids involved with wine or fixed or nonvolatile.",
        "volatile acidity: the amount of acetic acid in wine (high levels cause vinegar taste).",
        "citric acid: adds freshness and flavor to wines.",
        "residual sugar: the amount of sugar remaining after fermentation stops.",
        "chlorides: the amount of salt in the wine.",
        "free sulfur dioxide: prevents microbial growth and oxidation.",
        "total sulfur dioxide: amount of free and bound forms of SO2.",
        "density: the density of wine (close to water depending on alcohol/sugar content).",
        "pH: describes acidity (0-14 scale, most wines 2.9-3.9).",
        "sulphates: a wine additive, acts as antimicrobial and antioxidant.",
        "alcohol: the percent alcohol content of the wine.",
        "quality: score between 0-10 (target variable).",
        "The wine quality dataset contains physicochemical properties of red wines, with a quality score between 0 and 10.",
        "Alcohol content and volatile acidity are highly correlated with wine quality.",
        "Typical range of 'chlorides' is 0.012 to 0.611."
    ]

def load_context(dataset: str) -> List[str]:
    if dataset == "titanic":
        return titanic_context()
    elif dataset == "wine":
        return wine_context()
    raise ValueError(f"Unknown dataset: {dataset}")

def get_min_max_from_texts(texts, field):
    import re
    values = []
    for t in texts:
        try:
            if field in t:
                parts = t.split(";")
                for i, part in enumerate(parts):
                    if field in part.lower():
                        if i + 1 < len(parts):
                            val = parts[i+1].replace("\"", "").strip()
                            try:
                                values.append(float(val))
                            except Exception:
                                continue
        except Exception:
            continue
    if values:
        return min(values), max(values)
    return None, None

def load_models():
    global qa_pipeline, gen_pipeline
    try:
        qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
    except Exception as e:
        print("Warning: QA LLM pipeline could not be loaded!", e)
        qa_pipeline = None

    try:
        gen_pipeline = pipeline(
            "text-generation",
            model="microsoft/phi-2",
            torch_dtype=torch.float32,
            device="cuda" if torch.cuda.is_available() else "cpu"
        )
    except Exception as e:
        print("Warning: Generative LLM pipeline not loaded! Using QA only.", e)
        gen_pipeline = None

@app.on_event("startup")
def initialize_service():
    global vector_store, current_dataset
    current_dataset = "titanic"
    texts = load_context(current_dataset)
    embeddings = embed_texts(texts)
    vector_store = VectorStore(dim=embeddings.shape[1])
    vector_store.add(embeddings, texts)
    threading.Thread(target=load_models).start()  # Non-blocking model loading

@app.post("/rag_query", response_model=RagQueryResponse)
def handle_query(request: RagQueryRequest):
    global vector_store, current_dataset
    if not vector_store:
        raise HTTPException(503, "Vector store not initialized")
    query_embedding = embed_texts([request.query])[0]
    context_texts = vector_store.query(query_embedding, top_k=request.top_k)
    context_items = [ContextItem(text=text) for text in context_texts]
    synthesized_answer = generate_llm_answer(request.query, context_texts, current_dataset)
    return RagQueryResponse(
        query=request.query,
        contexts=context_items,
        synthesized_answer=synthesized_answer,
        dataset=current_dataset,
        context_count=len(context_texts)
    )

def generate_llm_answer(query: str, contexts: List[str], dataset: str) -> str:
    global qa_pipeline, gen_pipeline

    if gen_pipeline is not None and contexts:
        prompt = (
            "You are a helpful assistant for answering questions about tabular datasets. "
            "Use the provided context to answer the user's question. "
            "If the answer is a value range (e.g., min/max), try to infer it. "
            "If the context doesn't contain the answer, say so.\n\n"
            "Context:\n" + "\n".join(contexts) + f"\n\nQuestion: {query}\nAnswer:"
        )
        try:
            result = gen_pipeline(prompt, max_new_tokens=80, do_sample=False)[0]["generated_text"]
            if "Answer:" in result:
                answer = result.split("Answer:")[-1].strip().split("\n")[0]
            else:
                answer = result.strip()
            if answer and "not available" not in answer.lower():
                return answer
        except Exception as e:
            print("Gen LLM error:", e)

    if qa_pipeline is not None and contexts:
        context = " ".join(contexts)
        try:
            result = qa_pipeline(question=query, context=context)
            if result and result.get('answer', '').strip() and "not available" not in result['answer'].lower():
                return result['answer'].strip()
        except Exception as e:
            print("QA LLM error:", e)

    q = query.lower()
    if dataset == "titanic":
        if "who had a higher chance of survival" in q:
            return "Females had a much higher survival rate than males on the Titanic."
        if "how does age affect" in q:
            return "Children (younger passengers) had a higher survival rate than adults."
        if "pclass" in q and "mean" in q:
            return "Pclass refers to the ticket class: 1 = 1st, 2 = 2nd, 3 = 3rd."
        if "range of" in q:
            field = q.split("range of")[-1].split()[0].strip(" '\"")
            minv, maxv = get_min_max_from_texts(contexts, field)
            if minv is not None and maxv is not None:
                return f"{field} ranges from {minv} to {maxv}"
    elif dataset == "wine":
        if "what affects wine quality most" in q:
            return "Alcohol content and volatile acidity are most correlated with wine quality."
        if "residual sugar" in q:
            return "Residual sugar is the amount of sugar remaining after fermentation stops."
        if "range of 'chlorides'" in q or "range of chlorides" in q:
            return "Typical range of 'chlorides' is 0.012 to 0.611."
        if "range of" in q:
            field = q.split("range of")[-1].split()[0].strip(" '\"")
            minv, maxv = get_min_max_from_texts(contexts, field)
            if minv is not None and maxv is not None:
                return f"{field} ranges from {minv} to {maxv}"

    return (
        f"Relevant information about '{query}':\n"
        + "\n".join(f"- {ctx}" for ctx in contexts)
    )

@app.post("/switch_context")
def switch_context(request: ContextSwitchRequest):
    global vector_store, current_dataset
    try:
        texts = load_context(request.dataset)
        embeddings = embed_texts(texts)
        vector_store = VectorStore(dim=embeddings.shape[1])
        vector_store.add(embeddings, texts)
        current_dataset = request.dataset
        return {
            "status": "success",
            "dataset": request.dataset,
            "context_items": len(texts)
        }
    except ValueError as e:
        raise HTTPException(400, str(e))

@app.post("/ingest_csv")
async def ingest_csv_file(
    file: UploadFile = File(..., description="CSV file to ingest")
):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
            temp_file.write(await file.read())
            file_path = temp_file.name
        texts = ingest_csv(file_path, dataset=current_dataset)
        os.remove(file_path)
        if not texts:
            raise HTTPException(400, "No parsable text found in CSV")
        embeddings = embed_texts(texts)
        global vector_store
        vector_store = VectorStore(dim=embeddings.shape[1])
        vector_store.add(embeddings, texts)
        return {
            "status": "success",
            "filename": file.filename,
            "chunks": len(texts),
            "dataset": current_dataset
        }
    except Exception as e:
        raise HTTPException(500, f"Processing failed: {str(e)}")

@app.post("/ingest_pdf")
async def ingest_pdf_file(
    file: UploadFile = File(..., description="PDF file to ingest")
):
    if file.content_type != "application/pdf":
        raise HTTPException(400, "Only PDF files are accepted")
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(await file.read())
            file_path = temp_file.name
        texts = ingest_pdf(file_path)
        os.remove(file_path)
        if not texts:
            raise HTTPException(400, "No extractable text found in PDF")
        embeddings = embed_texts(texts)
        global vector_store
        vector_store = VectorStore(dim=embeddings.shape[1])
        vector_store.add(embeddings, texts)
        return {
            "status": "success",
            "filename": file.filename,
            "pages": len(texts),
            "dataset": current_dataset
        }
    except Exception as e:
        raise HTTPException(500, f"PDF processing failed: {str(e)}")

@app.get("/context_status")
def get_current_context():
    return {
        "dataset": current_dataset,
        "vector_store_ready": vector_store is not None,
        "service_version": app.version
    }

@app.get("/health", include_in_schema=False)
def health_check():
    return {
        "status": "healthy",
        "service": "RAG API",
        "version": app.version
    }

static_dir = pathlib.Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/demo", include_in_schema=False)
def rag_demo_page():
    return FileResponse(static_dir / "rag_query_demo.html")