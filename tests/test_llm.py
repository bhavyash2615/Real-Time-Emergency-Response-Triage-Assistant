from app.llm.llm_client import generate_triage

patient_history = """
Patient: Male, 62
History: Hypertension, Type 2 Diabetes, previous episode of chest pain.
Medications: Metformin, Lisinopril
"""

current_emergency = "Patient experiencing severe chest pain and shortness of breath."

result = generate_triage(patient_history, current_emergency)

print("\n=== TRIAGE RESULT ===\n")
print(result["recommendation"])
