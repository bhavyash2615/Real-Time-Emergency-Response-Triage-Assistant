import faiss
import json
import numpy as np
import json

# from embeddings.embedding_model import EmbeddingModel
from app.embeddings.embedding_model import EmbeddingModel

class ProtocolRetriever:

    def __init__(self):

        # load FAISS index
        self.index = faiss.read_index("disease_index.faiss")

        # load metadata
        with open("disease_metadata.json", "r") as f:
            self.metadata = json.load(f)

        # embedding model
        self.embedder = EmbeddingModel()

    def retrieve_protocols(self, query, top_k=20):
        """
        Retrieve most relevant disease protocols
        """

        # embed query
        if hasattr(self.embedder, "embed"):
            query_embedding = self.embedder.embed(query)
        else:
            model = self.embedder.get_model()
            query_embedding = model.encode(query)

        query_embedding = np.array([query_embedding]).astype("float32")

        distances, indices = self.index.search(query_embedding, top_k)

        results = []

        for idx in indices[0]:

            if idx < len(self.metadata):
                results.append(self.metadata[idx])

        return results
