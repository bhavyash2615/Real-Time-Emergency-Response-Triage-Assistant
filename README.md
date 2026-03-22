# Real-Time-Emergency-Response-Triage-Assistant
The Real-Time Emergency Response Triage Assistant is a system designed to support rapid decision-making in emergency scenarios. It processes patient history and current symptoms to generate structured triage recommendations in real time.
The system focuses on speed, relevance, and clarity by retrieving patient data, removing irrelevant information, classifying possible conditions, and generating actionable insights. It is particularly useful in environments where medical professionals must act quickly without reviewing large volumes of unstructured data.

## 📌 Problem Statement
In emergency rooms or disaster relief zones:
- Medical staff deal with massive, unstructured patient histories
- Protocol documents can be hundreds of pages long
- Critical decisions must be made instantly <br>
➡️ Traditional systems waste time processing irrelevant data.

## 🎯 Objective
Build a triage assistant that:
- ⚡ Retrieves + reasons in minimum latency
- 🧹 Removes irrelevant medical history (noise reduction)
- 🧠 Suggests next best medical action
- 🎤 Works with voice or text input

## ✨ Features
- 🔍 Intelligent Patient History Retrieval
Fetches complete patient records using a unique patient ID and organizes them into a usable format for downstream processing.
- ✂️ Intelligent Context Pruning
Filters out irrelevant or outdated medical data, ensuring that only context relevant to the current issue is retained.
- 🧠 ML-Based Condition Classification
Uses a trained Support Vector Machine (SVM) model to classify possible medical conditions based on symptoms and history.
- 🔗 Context-Aware Decision Support
Combines current symptoms with filtered patient history to improve prediction accuracy and relevance.
- 🤖 Contextual Reasoning Engine
Generates human-readable explanations and connects predictions with patient-specific context.
- 🚨 Emergency Triage Prioritization
Assigns urgency levels to help identify critical cases requiring immediate attention.
- 📋 Structured Actionable Output
Returns results in a clear format including condition, actions, and next steps.
- ⚡ Latency-Optimized Pipeline
Designed to minimize response time through efficient retrieval and pruning strategies.
- 🔎 Explainability & Transparency
Provides reasoning and highlights the patient context used in generating recommendations.

## 🛠 Tech Stack
- Frontend: HTML, CSS, JavaScript
- Backend: Python, REST API architecture
- AI / LLM: Large Language Model(LLM) API and ScaleDown API for token-efficient context compression
- Concepts: Retrieval-Augmented Generation (RAG)

## 📦 Installation & Setup
1. Clone the repository:<br>
git clone https://github.com/your-username/Real-Time-Emergency-Response-Triage-Assistant.git<br>
cd Real-Time-Emergency-Response-Triage-Assistant
2. Create and activate a virtual environment:<br>
python -m venv venv<br>
source venv/bin/activate<br>   # On Windows: venv\Scripts\activate
3. Install dependencies:<br>
pip install -r requirements.txt

## 🌍 Live Demo
🔗 Live Website: https://real-time-emergency-response-triage-assistant-ax42hkok1.vercel.app/
