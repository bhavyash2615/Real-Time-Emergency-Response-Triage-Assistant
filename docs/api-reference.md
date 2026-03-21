# API Reference

### 🔹 Base URL
```
http://localhost:8000
```

---

### 🔸 Endpoint: Triage Patient

**POST** `/triage`

Processes patient symptoms and history to generate a triage recommendation.

---

### 📥 Request Body

```json
{
  "patient_id": "string",
  "current_issue": "string"
}
```

#### Parameters

| Field           | Type   | Description                                      |
|-----------------|--------|--------------------------------------------------|
| patient_id      | string | Unique identifier for the patient                |
| current_issue   | string | Description of current symptoms or condition     |

---

### 📤 Response Body

```json
{
  "possible_condition": "string",
  "triage_level": "string",
  "actions": ["string"],
  "next_steps": ["string"],
  "llm_recommendation": "string",
  "timings": {
    "svm_protocol_ranking": "number",
    "llm_reasoning": "number"
  },
  "patient_context_used": {
    "diagnoses": ["string"],
    "medications": ["string"]
  },
  "latency_ms": "number",
  "step_times": {
    "history_retrieval": "number",
    "pruning": "number",
    "protocol_retrieval": "number",
    "triage_generation": "number"
  }
}
```

---

### 📊 Response Fields Explained

| Field                     | Description |
|--------------------------|------------|
| possible_condition       | Predicted medical condition based on symptoms and history |
| triage_level             | Urgency level (e.g., Immediate, Urgent, Non-Urgent) |
| actions                  | Immediate steps to be taken |
| next_steps               | Recommended diagnostic or clinical follow-ups |
| llm_recommendation       | Contextual explanation of the prediction |
| timings                  | Time taken for classification and reasoning steps |
| patient_context_used     | Relevant patient history used in decision-making |
| latency_ms               | Total response time in milliseconds |
| step_times               | Breakdown of time taken at each stage |

---

### ✅ Example Request

```bash
curl -X POST "http://localhost:8000/triage" \
-H "Content-Type: application/json" \
-d '{
  "patient_id": "10021118",
  "current_issue": "airway swelling and swollen throat"
}'
```

---

### ✅ Example Response

```json
{
  "possible_condition": "Anaphylaxis",
  "triage_level": "Immediate",
  "actions": [
    "inject epinephrine immediately if available",
    "call emergency services immediately"
  ],
  "next_steps": [
    "clinical diagnosis",
    "allergy testing"
  ]
}
```

---

### ⚠️ Error Responses

#### 400 Bad Request
```json
{
  "error": "Invalid input. Please provide patient_id and current_issue."
}
```

#### 404 Not Found
```json
{
  "error": "Patient not found."
}
```

#### 500 Internal Server Error
```json
{
  "error": "An unexpected error occurred."
}
```

---

### 🧪 Notes

- Ensure the backend server is running before making requests  
- Input should be concise but descriptive for better results  
- Latency may vary depending on dataset size and system load  

---
