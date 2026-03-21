from app.pruning.scaledown_client import compress_history

# Simulated large patient history
full_history = """
Patient: Male, 62
History:
- Hypertension for 10 years
- Type 2 Diabetes
- Previous chest pain episode in 2021
- Prescribed medications: Metformin, Lisinopril
- Family history of heart disease
- Reports occasional shortness of breath
"""

# Current emergency situation
current_issue = "Patient experiencing severe chest pain and sweating."

compressed = compress_history(full_history, current_issue)

print("\n=== COMPRESSED HISTORY ===\n")
print(compressed)
