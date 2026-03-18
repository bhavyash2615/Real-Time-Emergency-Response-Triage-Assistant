import os
import json
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

DISEASE_DATA_PATH = "data/diseases"

texts = []
labels = []

for file in os.listdir(DISEASE_DATA_PATH):

    if file.endswith(".json"):

        path = os.path.join(DISEASE_DATA_PATH, file)

        with open(path) as f:
            data = json.load(f)

        if "disease_name" not in data:
            print("❌ Missing disease_name in:", file)
            print("Keys found:", data.keys())
            continue

        disease = data["disease_name"]

        print("Training on:", disease)

        # Extract useful fields
        key_symptoms = " ".join(data.get("key_symptoms", []))
        other_symptoms = " ".join(data.get("other_symptoms", []))
        red_flags = " ".join(data.get("red_flags", []))
        risk_factors = " ".join(data.get("risk_factors", []))
        description = data.get("description", "")

        # Combine everything
        text = " ".join([
            key_symptoms,
            other_symptoms,
            red_flags,
            risk_factors,
            description
        ])

        texts.append(text)
        labels.append(disease)


# Vectorization
vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1,3),
    max_features=10000
)

X = vectorizer.fit_transform(texts)

# Train SVM
model = LinearSVC()

model.fit(X, labels)

# Save model
joblib.dump(model, "svm_disease_classifier.pkl")
joblib.dump(vectorizer, "svm_vectorizer.pkl")

print("SVM training complete")