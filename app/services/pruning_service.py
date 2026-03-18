import numpy as np
import json
from app.embeddings.embedding_model import EmbeddingModel


class PruningService:

    def __init__(self):

        self.embedder = EmbeddingModel()

        # max items to keep per category
        self.top_k = 5

        # # cache embeddings to avoid recomputing
        # self.embedding_cache = {}


    def prune_history(self, patient_history, current_issue):

        if patient_history is None:
            return None

        query_embedding = self._embed(current_issue)

        diagnoses = patient_history.get("diagnoses", [])[-20:]
        medications = patient_history.get("medications", [])[-20:]
        labs = patient_history.get("labs", [])[-20:]
        procedures = patient_history.get("procedures", [])[-20:]

        total_records = len(diagnoses) + len(medications) + len(labs) + len(procedures)
        if total_records <= self.top_k * 4:
            return patient_history

        # ---- combine everything for single embedding call ----
        all_records = diagnoses + medications + labs + procedures

        if not all_records:
            return patient_history
        
        if len(all_records) > 80:
            all_records = all_records[-80:]

        texts = [r if isinstance(r, str) else json.dumps(r) for r in all_records]

        record_embeddings = self._embed(texts)

        # ---- split embeddings back into categories ----
        d_len = len(diagnoses)
        m_len = len(medications)
        l_len = len(labs)

        diag_emb = record_embeddings[:d_len]
        med_emb = record_embeddings[d_len:d_len+m_len]
        lab_emb = record_embeddings[d_len+m_len:d_len+m_len+l_len]
        proc_emb = record_embeddings[d_len+m_len+l_len:]

        pruned_history = {
            "patient_id": patient_history["patient_id"],
            "age": patient_history.get("age"),
            "gender": patient_history.get("gender"),
            "relevant_diagnoses": self._filter_with_embeddings(diagnoses, diag_emb, query_embedding),
            "relevant_medications": self._filter_with_embeddings(medications, med_emb, query_embedding),
            "relevant_labs": self._filter_with_embeddings(labs, lab_emb, query_embedding),
            "relevant_procedures": self._filter_with_embeddings(procedures, proc_emb, query_embedding),
            "recent_admissions": patient_history.get("admissions", [])[-2:]
        }

        return pruned_history


    def _filter_with_embeddings(self, records, embeddings, query_embedding):

        if not records:
            return []

        if len(records) <= self.top_k:
            return records

        query_vec = np.array(query_embedding)
        record_vecs = np.array(embeddings)

        query_norm = np.linalg.norm(query_vec)
        record_norms = np.linalg.norm(record_vecs, axis=1)

        similarities = np.dot(record_vecs, query_vec) / (record_norms * query_norm)

        top_indices = np.argpartition(similarities, -self.top_k)[-self.top_k:]
        top_indices = top_indices[np.argsort(similarities[top_indices])[::-1]]

        return [records[i] for i in top_indices]


    def _embed(self, text):

        # ---- batch embedding directly ----
        if hasattr(self.embedder, "embed"):
            return self.embedder.embed(text)
        else:
            return self.embedder.model.encode(text)

        # if text in self.embedding_cache:
        #     return self.embedding_cache[text]

        # if hasattr(self.embedder, "embed"):
        #     emb = self.embedder.embed(text)
        # else:
        #     emb = self.embedder.model.encode(text)

        # self.embedding_cache[text] = emb

        # return emb