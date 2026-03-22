# Real Time Emergency Response Triage Assistant
A smart clinical triage system that analyzes patient symptoms and history to suggest possible conditions, urgency level, and recommended actions using a combination of LLM reasoning and machine learning models.<br>
🔗 Live Demo: https://real-time-emergency-response-triage.vercel.app/ <br>
🔗 Backend API: Hosted on Render [https://real-time-emergency-response-triage.onrender.com/docs]

This documentation will guide and help you understand, set up, and use the application effectively.

---

## 📚 Documentation

- [Getting Started](docs/getting-started.md)
- [Features](docs/features.md)
- [Architecture](docs/architecture.md)
- [API Reference](docs/api-reference.md)
- [Configuration](docs/configuration.md)
- [User Guide](docs/user-guide.md)
- [Contributing](docs/contributing.md)
- [Troubleshooting](docs/troubleshooting.md)

---

## Quick Link 
[Github Repository](https://github.com/bhavyash2615/Real-Time-Emergency-Response-Triage-Assistant)

---

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

---

## 🛠 Tech Stack
### Backend
- FastAPI – High-performance API framework for low-latency responses
- Uvicorn – ASGI server for running FastAPI
- Python – Core backend language
### AI / Machine Learning
- LLM (Groq/ Gemini)
- Used for medical reasoning and decision explanation
- Optimized with context pruning to reduce latency
- Scikit-learn (SVM Classifier)
- Fast triage classification (Low / Moderate / Urgent)
### Retrieval & Embeddings
- Vector Database (FAISS / custom vector client)
- Stores embeddings of:<br>
Patient history<br>
Medical protocols<br>
- Embedding Model<br>
Converts text → vectors for semantic search
### Core Optimization Layer
- Intelligent Context Pruning (Custom Service)
- Removes irrelevant medical history
- Reduces token size before LLM call
### Data Processing
- Custom Ingestion Pipelines
- MIMIC dataset ingestion
- Disease protocol ingestion
- Chunking for vector storage
### Storage
- Custom Patient Database (patient_db.py)
- Stores structured patient records
- Vector Store (vector_db/)
- Handles similarity-based retrieval
### Utilities
- Latency Timer
- Measures response time per request
- Context Builder
### Frontend (Optional / External)
HTML, CSS, JavaScript
### Deployment
- Render - Backend
- Vercel - Frontend

---

## ⚙️ How It Works
1. Input<br>
- Symptoms (text or voice)<br>
- Patient ID
2. Retrieval
- Fetch patient history<br>
- Fetch relevant medical protocols<br>
3. Context Pruning (🔥 Key Step)<br>
- Remove irrelevant records
- Rank important medical signals
- Compress context
4. Parallel Processing
- SVM Model → triage classification
- LLM → reasoning + explanation
5. Triage Output
- Disease , relevant patient history and llm recommendation

---

## 📁 Project Structure
```bash
real-time-emergency-response-triage-assistant/
│
├── app/                             # Core backend application (FastAPI)
│   ├── main.py                      # Entry point (FastAPI app)
│   ├── config.py                    # Environment configs & constants
│   ├── __init__.py                  # App initializer
│
│   ├── api/                         # API layer (routes/controllers)
│   │   └── triage_routes.py         # Triage endpoints (POST /triage)
│
│   ├── services/                    # Business logic layer
│   │   ├── triage_service.py        # Orchestrates full triage pipeline
│   │   ├── patient_service.py       # Handles patient data retrieval
│   │   ├── vector_service.py        # Handles vector DB queries
│   │   └── pruning_service.py       # 🔥 Intelligent context pruning logic
│
│   ├── retrieval/                   # Data retrieval layer
│   │   ├── history_retriever.py     # Fetch patient history
│   │   └── protocol_retriever.py    # Fetch medical protocols
│
│   ├── reasoning/                   # Decision-making logic
│   │   └── triage_reasoner.py       # Combines LLM + ML outputs
│
│   ├── llm/                         # LLM integration
│   │   └── llm_client.py            # Handles LLM API calls (Gemini/Phi-3)
│
│   ├── ml/                          # Machine learning models
│   │   ├── svm_classifier.py        # SVM model for triage classification
│   │   └── train_svm_classifier.py  # Training script for SVM
│
│   ├── embeddings/                  # Embedding generation
│   │   └── embedding_model.py       # Converts text → vector embeddings
│
│   └── utils/                       # Utility/helper functions
│       ├── context_builder.py       # Builds optimized LLM input
│       └── latency_timer.py         # Measures response latency
│
├── ingestion/                       # Data ingestion pipelines
│   ├── ingest_mimic.py              # Load MIMIC dataset
│   ├── ingest_diseases.py           # Load disease/protocol data
│   └── chunking.py                  # Text chunking for embeddings
│
├── retrieval_tests/                 # (Optional) Retrieval testing/debugging
│   └── test_retrieval.py            # Validate retrieval quality
│
├── database/                        # Structured data storage
│   └── patient_db.py                # Patient records management
│
├── vector_db/                       # Vector database integration
│   └── vector_client.py             # FAISS / vector DB wrapper
│
├── data/                            # Raw and processed datasets
│   ├── patients/                    # Patient history data
│   └── diseases/                    # Disease & protocol documents
│
├── frontend/                        # Frontend (UI layer)
│   ├── index.html                   # Main UI
│   ├── style.css                    # Styling
│   ├── script.js                    # API calls + UI logic
│   └── assets/                      # Images/icons (optional)
│
├── docs/                            # Documentation
│   ├── architecture.md              # System design & flow
│   ├── api-reference.md             # API details
│   ├── setup.md                     # Installation guide
│   ├── pruning-explained.md         # 🔥 Core idea explanation
│   └── troubleshooting.md           # Common issues
│
├── tests/                           # Unit & integration tests
│   ├── test_api.py                  # API testing
│   ├── test_pruning.py              # Context pruning validation
│   └── test_latency.py              # Latency benchmarks
│
├── requirements.txt                 # Python dependencies
├── .env.example                     # Sample environment variables
├── .gitignore                       # Ignored files
├── README.md                        # Project overview
└── venv/                            # Local virtual environment (ignored)
```

---
