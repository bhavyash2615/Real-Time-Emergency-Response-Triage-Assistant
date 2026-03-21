from app.ml.svm_classifier import predict_disease

tests = [
    "fever neck stiffness",
    "severe chest pain sweating nausea",
    "difficulty breathing wheezing"
]

for t in tests:

    print("Symptoms:", t)
    print("Prediction:", predict_disease(t))
    print()