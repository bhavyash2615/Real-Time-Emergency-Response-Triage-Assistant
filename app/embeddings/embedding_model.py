from sentence_transformers import SentenceTransformer
from app.config import EMBEDDING_MODEL

class EmbeddingModel:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)

    def embed_text(self, text: str):
        return self.model.encode(text).tolist()

    def embed_batch(self, texts):
        return self.model.encode(texts).tolist()

