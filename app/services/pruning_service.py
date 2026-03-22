import numpy as np
import json
from app.embeddings.embedding_model import EmbeddingModel


class PruningService:

    def __init__(self):

        self.embedder = EmbeddingModel()

        # max items to keep per category
        self.top_k = 3

        # # cache embeddings to avoid recomputing
        # self.embedding_cache = {}
        self.query_cache = {}


    def prune_history(self, patient_history, current_issue):

        if patient_history is None:
            return None

        if current_issue in self.query_cache:
            query_embedding = self.query_cache[current_issue]
        else:
            query_embedding = self._embed(current_issue)
            self.query_cache[current_issue] = query_embedding

        diagnoses = self._keyword_filter(
            patient_history.get("diagnoses", []),
            current_issue,
            max_keep=5
        )[-10:]

        medications = self._keyword_filter(
            patient_history.get("medications", []),
            current_issue,
            max_keep=7
        )[-10:]

        labs = self._keyword_filter(
            patient_history.get("labs", []),
            current_issue,
            max_keep=3
        )[-10:]

        procedures = self._keyword_filter(
            patient_history.get("procedures", []),
            current_issue,
            max_keep=5
        )[-10:]

        if len(medications) < 3:
            medications = patient_history.get("medications", [])[-3:]

        # -------- QUICK KEYWORD CHECK --------
        all_filtered = diagnoses + medications + labs + procedures

        query_words = set(current_issue.lower().split())

        match_count = 0

        for r in all_filtered:
            text = str(r).lower()
            for word in query_words:
                if word in text:
                    match_count += 1
                    break

        # if enough matches → skip embedding
        if match_count >= 4:
            return {
                "patient_id": patient_history["patient_id"],
                "age": patient_history.get("age"),
                "gender": patient_history.get("gender"),
                "relevant_diagnoses": diagnoses,
                "relevant_medications": medications,
                "relevant_labs": labs,
                "relevant_procedures": procedures,
                "recent_admissions": patient_history.get("admissions", [])[-2:]
            }

        total_records = len(diagnoses) + len(medications) + len(labs) + len(procedures)

        if total_records <= self.top_k * 4:
            return patient_history

        # ---- combine everything for single embedding call ----
        # limit per category instead of global cut
        diagnoses = diagnoses[:3]
        medications = medications[:3]
        labs = labs[:1]
        procedures = procedures[:1]

        all_records = diagnoses + medications + labs + procedures

        if not all_records or len(all_records) <= self.top_k:
            return patient_history

        texts = [str(r) for r in all_records]

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
    
    def _keyword_filter(self, records, query, max_keep=15):

        if not records:
            return []

        query_words = set(query.lower().split())

        scored = []

        for r in records:
            text = str(r).lower()
            score = sum(1 for word in query_words if word in text)
            scored.append((score, r))

        scored.sort(reverse=True, key=lambda x: x[0])

        top = [r[1] for r in scored[:max_keep]]

        # fallback to recent if needed
        if len(top) < 5:
            needed = 5 - len(top)
            top += records[-needed:]

        return top
    


    def _filter_with_embeddings(self, records, embeddings, query_embedding):

        # handle empty cases safely
        if not records or embeddings is None or len(embeddings) == 0:
            return []

        if len(records) <= self.top_k:
            return records

        # convert to numpy arrays
        query_vec = np.array(query_embedding)
        record_vecs = np.array(embeddings)

        # safety check for invalid shapes
        if record_vecs.ndim != 2 or record_vecs.shape[0] == 0:
            return records[:self.top_k]

        try:
            similarities = np.dot(record_vecs, query_vec)
        except Exception:
            # fallback if something goes wrong
            return records[:self.top_k]

        # get top-k indices
        top_indices = np.argpartition(similarities, -self.top_k)[-self.top_k:]
        top_indices = top_indices[np.argsort(similarities[top_indices])[::-1]]

        result = [records[i] for i in top_indices]

        # ensure minimum output
        if len(result) < 3 and len(records) >= 3:
            result = records[:3]

        return result


    def _embed(self, text):

        if isinstance(text, list):
            return self.embedder.embed_batch(text)

        return self.embedder.embed_text(text)