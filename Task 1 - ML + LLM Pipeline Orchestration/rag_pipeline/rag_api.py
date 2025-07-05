from fastapi import FastAPI, Request
from embed import embed_texts
from vector_store import VectorStore

app = FastAPI()

# In-memory store for demo
texts = ["The Eiffel Tower is in Paris.", "The Taj Mahal is in India.", "Mount Everest is the tallest mountain."]
embeddings = embed_texts(texts)
store = VectorStore(dim=embeddings.shape[1])
store.add(embeddings, texts)

@app.post("/rag_query")
async def rag_query(request: Request):
    req = await request.json()
    query = req.get('query')
    query_emb = embed_texts([query])
    results = store.query(query_emb[0])
    # For demo: just return retrieved context
    return {"context": results, "answer": "LLM answers here (stub)"}

@app.get("/")
def root():
    return {"status": "RAG Service is running!"}