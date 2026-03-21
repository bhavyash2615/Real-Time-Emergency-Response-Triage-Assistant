from sentence_transformers import SentenceTransformer
from app.config import EMBEDDING_MODEL


class EmbeddingModel:
    def __init__(self):
        self.model = None

    def get_model(self):
        if self.model is None:
            self.model = SentenceTransformer(EMBEDDING_MODEL)
        return self.model

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