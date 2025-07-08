import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional
import os
from config import config
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

class ChromaManager:
    def __init__(self):
        try:
            self.client = chromadb.PersistentClient(
                path=config['CHROMA_PERSIST_DIR'],
                settings=Settings(allow_reset=True)
            )
            self.collection = self.client.get_or_create_collection(
                name="web3_articles",
                metadata={"hnsw:space": "cosine"}
            )
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self.available = True
        except Exception as e:
            print(f"ChromaDB initialization failed: {e}")
            self.available = False

    def add_articles(self, articles: List[Dict]):
        if not self.available or not articles:
            return

        try:
            embeddings = self.model.encode([a['title'] for a in articles])
            self.collection.add(
                embeddings=[emb.tolist() for emb in embeddings],
                documents=[a['title'] for a in articles],
                metadatas=[{
                    'url': a['url'],
                    'source': a['source']
                } for a in articles],
                ids=[str(hash(a['url'])) for a in articles]
            )
        except Exception as e:
            print(f"Failed to add articles to ChromaDB: {e}")

    def query_similar(self, title: str, threshold: float = 0.8) -> Optional[Dict]:
        if not self.available:
            return None

        try:
            query_embedding = self.model.encode([title])[0].tolist()
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=1
            )
            
            if results and results['distances'][0] and results['distances'][0][0] >= threshold:
                return {
                    'title': results['documents'][0][0],
                    'url': results['metadatas'][0][0]['url'],
                    'source': results['metadatas'][0][0]['source']
                }
        except Exception as e:
            print(f"ChromaDB query failed: {e}")
        
        return None