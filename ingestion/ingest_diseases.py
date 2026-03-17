import faiss
import json
import os
import numpy as np   # NEW

from app.config import DISEASE_DATA_PATH
from ingestion.chunking import chunk_text
from app.embeddings.embedding_model import EmbeddingModel
from vector_db.vector_client import VectorClient


def ingest_diseases():
    embedder = EmbeddingModel()
    vector_db = VectorClient()

    all_embeddings = []   # NEW
    metadata = []         # NEW

    for file in os.listdir(DISEASE_DATA_PATH):

        if not file.endswith(".json"):
            continue

        path = os.path.join(DISEASE_DATA_PATH, file)

        with open(path, "r") as f:
            data = json.load(f)

        disease_name = data.get("disease_name", file.replace(".json", ""))

        text = json.dumps(data)

        chunks = chunk_text(text)

        embeddings = embedder.embed_batch(chunks)

        metadatas = [
            {
                "disease": disease_name,
                "text": chunk
            }
            for chunk in chunks
        ]

        vector_db.add(embeddings, metadatas)

        # NEW — collect for FAISS save
        all_embeddings.extend(embeddings)
        metadata.extend(metadatas)

    vector_db.save()

    # NEW — build FAISS index
    embeddings_np = np.array(all_embeddings).astype("float32")
    dimension = embeddings_np.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings_np)

    # Save FAISS index
    faiss.write_index(index, "disease_index.faiss")

    # Save metadata
    with open("disease_metadata.json", "w") as f:
        json.dump(metadata, f)

    print("Disease ingestion completed")


if __name__ == "__main__":
    ingest_diseases()
