from sentence_transformers import SentenceTransformer
from app.config import EMBEDDING_MODEL

_model = None   # GLOBAL CACHE


class EmbeddingModel:
    def __init__(self):
        pass

    def get_model(self):
        global _model
        if _model is None:
            print("Loading embedding model...")
            _model = SentenceTransformer(EMBEDDING_MODEL)
        return _model

    def embed_text(self, text: str):
        model = self.get_model()
        return model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

    def embed_batch(self, texts):
        model = self.get_model()
        return model.encode(
            texts,
            batch_size=32,
            convert_to_numpy=True,
            normalize_embeddings=True
        )