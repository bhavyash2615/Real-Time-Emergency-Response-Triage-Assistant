import ast
import json
import os
from app.llm.llm_client import generate_triage
from app.config import DISEASE_DATA_PATH
from app.ml.svm_classifier import predict_disease
import time

class TriageReasoner:

    def __init__(self):
        pass

    def rank_protocols(self, protocols, query):

        predicted = predict_disease(query)

        print("SVM predicted protocol:", predicted)

        # 1️⃣ First try matching within retrieved protocols (RAG results)
        for protocol in protocols:

            raw = protocol.get("text", "")

            try:
                data = json.loads(raw)
            except:
                continue

            disease = data.get("disease_name", "").lower()

            if predicted.lower() in disease:
                print("Matched retrieved protocol:", disease)

                return {
                    "disease": disease,
                    "text": json.dumps(data)
                }

        # 2️⃣ If not found, search full disease folder
        for file in os.listdir(DISEASE_DATA_PATH):

            if file.endswith(".json"):

                path = os.path.join(DISEASE_DATA_PATH, file)

                with open(path, encoding="utf-8") as f:
                    data = json.load(f)

                disease = data.get(
                    "disease_name",
                    file.replace(".json", "")
                )

                if predicted.lower() in disease.lower():

                    print("Matched protocol from disk:", disease)

                    return {
                        "disease": disease,
                        "text": json.dumps(data)
                    }

        # 3️⃣ Fallback
        print("No SVM match found, using first retrieved protocol")

        return protocols[0]

    def generate_triage(self, current_issue, pruned_history, protocols):

        def clean_list(values):
            seen = set()
            cleaned = []

            for v in values:
                normalized = v.strip().lower()

                if normalized not in seen:
                    seen.add(normalized)
                    cleaned.append(v)

            return cleaned  
       
        if not protocols:
            return {
                "triage_level": "unknown",
                "possible_condition": None,
                "recommended_medication": [],
                "next_steps": [],
                "patient_context_used": {
                    "diagnoses": diagnoses,
                    "medications": medications
                }
            }

        # Select best protocol
        svm_start = time.time()

        top_protocol = self.rank_protocols(protocols, current_issue)

        svm_time = round((time.time() - svm_start) * 1000, 2)

        if top_protocol is None:
            top_protocol = protocols[0]

        protocol_data = {}

        if "text" in top_protocol:

            raw = top_protocol.get("text", "")

            # Fix truncated JSON
            if raw.strip().endswith('"source":'):
                raw = raw + ' "unknown"}'

            if not raw.strip().endswith("}"):
                raw = raw + "}"

            try:
                protocol_data = json.loads(raw)

            except Exception as e:
                print("JSON PARSE ERROR:", e)
                protocol_data = {}

        print("PARSED PROTOCOL DATA:")
        print(protocol_data.keys())

        triage_level = protocol_data.get(
            "triage_priority",
            protocol_data.get("triage_level", "unknown")
        )

        actions = protocol_data.get("actions", [])

        next_steps = (
            protocol_data.get("common_tests")
            or protocol_data.get("diagnostic_tests")
            or protocol_data.get("tests")
            or []
        )

        recommended_medication = []

        for action in actions:
            text = str(action).lower()

            if any(keyword in text for keyword in [
                "aspirin",
                "nitro",
                "medication",
                "chew",
                "administer",
                "inject"
            ]):
                recommended_medication.append(action)

        print("Loaded condition:", protocol_data.get("disease_name"))
        print("Loaded actions count:", len(protocol_data.get("actions", [])))

        # Patient history context
        diagnoses = clean_list(pruned_history.get("relevant_diagnoses", []))[:3]
        medications = clean_list(pruned_history.get("relevant_medications", []))[:3]

        
        context = (
            f"{protocol_data.get('disease_name')} | "
            f"{current_issue} | "
            f"{', '.join(diagnoses[:2])} | "
            f"{', '.join(medications[:1])}"
        )

        # LLM reasoning step
        llm_start = time.time()
        llm_result = generate_triage(context)
        llm_time = round((time.time() - llm_start) * 1000, 2)


        return {
            "possible_condition": protocol_data.get(
                "disease_name",
                top_protocol.get("disease")
            ),
            "triage_level": triage_level,
            "actions": actions,
            "next_steps": next_steps,
            "llm_recommendation": llm_result["recommendation"],
            "timings": {
                "svm_protocol_ranking": svm_time,
                "llm_reasoning": llm_time
            },
            "patient_context_used": {
                "diagnoses": diagnoses,
                "medications": medications
            }
        }
