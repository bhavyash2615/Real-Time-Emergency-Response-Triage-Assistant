from app.pruning.scaledown_client import compress_history
from app.retrieval.history_retriever import HistoryRetriever
from app.retrieval.protocol_retriever import ProtocolRetriever
from app.services.pruning_service import PruningService
from app.reasoning.triage_reasoner import TriageReasoner
import time
import json

def count_tokens(text):

    if text is None:
        return 0

    if isinstance(text, dict):
        text = json.dumps(text)

    return int(len(text) / 4)  # Rough estimate: 1 token ~ 4 characters


class TriageService:

    def __init__(self):

        self.history_retriever = HistoryRetriever()
        self.protocol_retriever = ProtocolRetriever()
        self.pruner = PruningService()
        self.reasoner = TriageReasoner()

    def run_triage(self, patient_id, current_issue):
        """
        Full triage pipeline
        """
        start_time = time.time()
        step_times = {}

        # -------------------------
        # Step 1: Retrieve patient history
        # -------------------------
        t = time.time()
        patient_history = self.history_retriever.get_patient_history(patient_id)
        step_times["history_retrieval"] = round((time.time() - t)*1000, 3)

        if patient_history is None:
            return {"error": "Patient not found"}
        
        # -------------------------
        # Step 2: Compress history using Scaledown
        # -------------------------

        # tokens_before_scaledown = count_tokens(patient_history)
        # t = time.time()
        # compressed_history = compress_history(patient_history, current_issue)
       
        # tokens_after_scaledown = count_tokens(compressed_history)
        # step_times["scaledown_compression"] = round((time.time() - t)*1000, 3)
        compressed_history = patient_history

 
        # -------------------------
        # Step 2: Context pruning
        # -------------------------
        t = time.time()
        pruned_history = self.pruner.prune_history(
            compressed_history,
            current_issue
        )
        step_times["pruning"] = round((time.time() - t)*1000, 3)

        # -------------------------
        # Step 3: Retrieve protocols (RAG)
        # -------------------------
        t = time.time()
        protocols = self.protocol_retriever.retrieve_protocols(
            current_issue
        )
        step_times["protocol_retrieval"] = round((time.time() - t)*1000, 3)

        # -------------------------
        # Step 4: Generate triage decision
        # -------------------------
        t = time.time()
        result = self.reasoner.generate_triage(
            current_issue,
            pruned_history,
            protocols
        )
        step_times["triage_generation"] = round((time.time() - t)*1000, 3)

        total_latency = round(time.time() - start_time, 3)
        latency_ms = round(total_latency * 1000, 2)
        result["latency_ms"] = latency_ms
        result["step_times"] = step_times

        # result["token_usage"] = {
        #     "before_scaledown": tokens_before_scaledown,
        #     "after_scaledown": tokens_after_scaledown,
        #     "reduction_percent": round(
        #         (1 - tokens_after_scaledown / tokens_before_scaledown) * 100, 2
        #     ) if tokens_before_scaledown else 0
        # }

        print("\n------ TRIAGE PIPELINE LATENCY ------")

        for step, duration in step_times.items():
            print(f"{step}: {duration} ms")

        print(f"TOTAL LATENCY: {total_latency * 1000} ms")

        print("-------------------------------------\n")

        return result

    def get_all_patient_ids(self):
        return self.history_retriever.get_all_patient_ids()