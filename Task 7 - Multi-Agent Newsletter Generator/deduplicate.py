from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

def deduplicate_articles(articles, threshold=0.8):
    if not articles:
        return []
    model = SentenceTransformer('all-MiniLM-L6-v2')
    titles = [a['title'] for a in articles]
    embeddings = model.encode(titles, convert_to_numpy=True)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    unique_indices = []
    for idx, emb in enumerate(embeddings):
        if not unique_indices:
            index.add(np.expand_dims(emb, 0))
            unique_indices.append(idx)
            continue
        D, _ = index.search(np.expand_dims(emb, 0), len(unique_indices))
        if D[0].max(initial=0) < threshold:
            index.add(np.expand_dims(emb, 0))
            unique_indices.append(idx)
    deduped = [articles[i] for i in unique_indices]
    return deduped