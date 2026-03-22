from sentence_transformers import SentenceTransformer
from app.config import EMBEDDING_MODEL

# GLOBAL MODEL (loaded once at startup)
_model = SentenceTransformer(EMBEDDING_MODEL)


class EmbeddingModel:

    def embed_text(self, text: str):
        return _model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

    def embed_batch(self, texts):
        return _model.encode(
            texts,
            batch_size=32,
            convert_to_numpy=True,
            normalize_embeddings=True
        )