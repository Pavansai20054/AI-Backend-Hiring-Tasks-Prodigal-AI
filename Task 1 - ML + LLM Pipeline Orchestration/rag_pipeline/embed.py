from sentence_transformers import SentenceTransformer

# Singleton model to avoid repeated loading
_model = None

def get_model(model_name="all-MiniLM-L6-v2"):
    global _model
    if _model is None:
        _model = SentenceTransformer(model_name)
    return _model

def embed_texts(texts, model_name="all-MiniLM-L6-v2"):
    model = get_model(model_name)
    embeddings = model.encode(texts)
    return embeddings