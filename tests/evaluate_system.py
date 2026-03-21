from app.services.triage_service import TriageService
from app.utils.accuracy_tracker import AccuracyTracker

triage_service = TriageService()
tracker = AccuracyTracker()

total_latency = 0
total_token_before = 0
total_token_after = 0

test_cases = [

    {
        "patient_id": "10039831",
        "symptoms": "sudden vision problems and trouble walking",
        "true_condition": "Stroke"
    },

    {
        "patient_id": "10039831",
        "symptoms": "severe allergic reaction and difficulty breathing",
        "true_condition": "Anaphylaxis"
    },

    {
        "patient_id": "10039831",
        "symptoms": "high fever, confusion and infection",
        "true_condition": "Sepsis"
    }

]

for case in test_cases:

    result = triage_service.run_triage(
        case["patient_id"],
        case["symptoms"]
    )

    predicted = result["possible_condition"]
    actual = case["true_condition"]

    tracker.update(predicted, actual)

    total_latency += result["latency_ms"]

    token_usage = result.get("token_usage", {})
    total_token_before += token_usage.get("before_scaledown", 0)
    total_token_after += token_usage.get("after_scaledown", 0)


num_cases = len(test_cases)

print("\n========= SYSTEM EVALUATION =========\n")

print("Total Test Cases:", num_cases)

print("Accuracy:", tracker.get_accuracy(), "%")

print("Average Latency:",
      round(total_latency / num_cases, 2),
      "ms")

print("Average Tokens Before Scaledown:",
      round(total_token_before / num_cases, 2))

print("Average Tokens After Scaledown:",
      round(total_token_after / num_cases, 2))

print("Average Token Reduction:",
      round(
          (1 - (total_token_after / total_token_before)) * 100,
          2
      ),
      "%"
)
