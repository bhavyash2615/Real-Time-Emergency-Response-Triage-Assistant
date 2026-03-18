import joblib
import os

BASE_DIR = os.path.dirname(__file__)

model = joblib.load(os.path.join(BASE_DIR, "svm_disease_classifier.pkl"))
vectorizer = joblib.load(os.path.join(BASE_DIR, "svm_vectorizer.pkl"))


def predict_disease(symptoms_text):

    X = vectorizer.transform([symptoms_text])

    prediction = model.predict(X)[0]

    return prediction