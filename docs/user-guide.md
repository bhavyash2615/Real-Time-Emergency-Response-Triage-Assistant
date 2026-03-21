# User Guide  
## Real-Time Emergency Response Triage Assistant

---

## 🧭 Introduction

The Real-Time Emergency Response Triage Assistant is designed to help quickly assess medical situations by analyzing patient history and current symptoms. It provides structured recommendations including possible conditions, urgency level, and immediate actions.

This guide explains how to use the system effectively.

---

## 🚀 Getting Started

### Step 1: Open the Application
- Launch the frontend interface in your browser  
- Ensure the backend server is running  

---

### Step 2: Enter Patient Details

You will see input fields for:

- **Patient ID** → Enter a valid patient identifier  
- **Current Issue / Symptoms** → Describe the patient’s current condition  

✅ Example:
```
Patient ID: 10021118  
Symptoms: airway swelling and swollen throat
```

---

### Step 3: Submit the Request

- Click the **“Analyze” / “Run Triage”** button  
- The system will process the input and generate a response  

---

## 📊 Understanding the Output

The system returns a structured response with the following components:

---

### 🔹 Possible Condition
- Predicted medical condition based on symptoms and history  

---

### 🔹 Triage Level
- Indicates urgency of the situation  
- Common levels:
  - **Immediate** → Requires urgent attention  
  - **Urgent** → Needs quick evaluation  
  - **Non-Urgent** → Lower priority  

---

### 🔹 Recommended Actions
- Immediate steps to take in the current situation  
- Designed for quick response  

---

### 🔹 Next Steps
- Suggested diagnostic or clinical follow-ups  
- Helps guide further medical evaluation  

---

### 🔹 Explanation
- Provides reasoning behind the prediction  
- Connects symptoms with patient history  

---

### 🔹 Patient Context Used
- Shows relevant diagnoses and medications  
- Helps understand what influenced the decision  

---

### 🔹 Performance Metrics
- Displays processing time and latency  
- Useful for monitoring system performance  

---

## 💡 Tips for Best Results

- Provide **clear and specific symptoms**  
- Use a **valid patient ID** present in the dataset  
- Avoid overly vague inputs (e.g., “not feeling well”)  
- Use example prompts if unsure how to start  

---

## ⚠️ Important Notes

- This system is a **decision-support tool**, not a replacement for medical professionals  
- Always verify results with qualified healthcare providers  
- Output accuracy depends on data quality and input clarity  

---

## 🧪 Example Use Case

**Input:**
```
Patient ID: 10021118  
Symptoms: airway swelling and difficulty breathing
```

**Output:**
- Condition: Anaphylaxis  
- Triage Level: Immediate  
- Actions: Administer epinephrine, call emergency services  

---

## ❓ Common Questions

### What if I don’t know the patient ID?
You must use a valid patient ID available in the dataset for accurate results.

---

### Can I input multiple symptoms?
Yes, you can describe multiple symptoms in a single input field.

---

### How fast is the system?
The system is designed for **real-time response**, typically within milliseconds to a second depending on load.

---

### Why is some history not shown?
The system removes irrelevant data to focus only on what matters for the current condition.

---

## 🛠️ Need Help?

If you encounter issues:
- Check the **README Troubleshooting section**  
- Ensure backend server is running  
- Verify your input format  

---

## 📌 Summary

This system helps you:
- Quickly analyze patient data  
- Identify possible conditions  
- Understand urgency levels  
- Take immediate action  

All within a fast and structured workflow designed for emergency scenarios.

---
