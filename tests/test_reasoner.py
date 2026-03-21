from app.reasoning.triage_reasoner import TriageReasoner
import json

reasoner = TriageReasoner()

mock_protocol = {
    "text": json.dumps({
        "disease_name": "Myocardial Infarction",
        "triage_priority": "CRITICAL",
        "key_symptoms": ["chest pain", "shortness of breath"],
        "actions": [
            "Administer aspirin",
            "Monitor ECG",
            "Provide oxygen"
        ],
        "common_tests": ["ECG", "Troponin blood test"]
    })
}

result = reasoner.generate_triage(
    current_issue="severe chest pain and sweating",
    pruned_history={
        "relevant_diagnoses": ["hypertension"],
        "relevant_medications": ["lisinopril"]
    },
    protocols=[mock_protocol]
)

print(result)
