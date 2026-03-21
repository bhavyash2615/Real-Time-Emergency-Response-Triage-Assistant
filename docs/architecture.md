# Architecture

This document describes the technical architecture of **Real Time Emergency Response Triage Assistant**,
including system components, data flow, and key design decisions.

## System Overview

Emergency Triage Assistant follows a layered architecture where each component
has a single, well-defined responsibility.

Below is a high-level logical layout of the system:
```bash
┌──────────────────────────────┐
│          Frontend            │
│   (Web UI / Interface)       │
│                              │
│ • Patient ID input           │
│ • Symptom input              │
│ • Example case prompts       │
│ • Triage result display      │
└───────────────┬──────────────┘
                │ HTTP (JSON)
                ▼
┌──────────────────────────────┐
│           Backend            │
│        (FastAPI / API)       │
│                              │
│ • Input validation           │
│ • Request routing            │
│ • Pipeline orchestration     │
└───────────────┬──────────────┘
                │
                ▼
┌──────────────────────────────┐
│     History Retrieval Layer  │
│                              │
│ • Fetch patient records      │
│ • Access database (MIMIC)    │
│ • Retrieve full history      │
└───────────────┬──────────────┘
                │
                ▼
┌──────────────────────────────┐
│   Context Pruning Engine     │
│                              │
│ • Remove irrelevant data     │
│ • Filter outdated records    │
│ • Build focused context      │
└───────────────┬──────────────┘
                │
                ▼
┌──────────────────────────────┐
│   ML Classification Layer    │
│    (SVM Classifier)          │
│                              │
│ • Symptom analysis           │
│ • Pattern matching           │
│ • Condition prediction       │
└───────────────┬──────────────┘
                │
                ▼
┌──────────────────────────────┐
│   Protocol Retrieval (RAG)   │
│                              │
│ • Fetch relevant diseases    │
│ • Retrieve medical protocols │
│ • Vector similarity search   │
└───────────────┬──────────────┘
                │
                ▼
┌──────────────────────────────┐
│   Contextual Reasoning Layer │
│                              │
│ • Combine condition + history│
│ • Generate explanation       │
│ • Refine triage output       │
└───────────────┬──────────────┘
                │
                ▼
┌──────────────────────────────┐
│        Triage Output         │
│                              │
│ • Possible condition         │
│ • Triage level               │
│ • Immediate actions          │
│ • Next steps                 │
│ • Reasoning explanation      │
│ • Latency metrics            │
└───────────────┬──────────────┘
                │
                ▼
┌──────────────────────────────┐
│          Frontend UI         │
│                              │
│ • Displays structured output │
│ • Highlights key actions     │
│ • Shows reasoning + context  │
└──────────────────────────────┘

```

---

## 🧩 High-Level Overview

The system consists of three primary layers:

1. **Frontend (Client Interface)**
2. **Backend (API Server)**
3. **Data Processing & Decision Pipeline**

Each layer is designed to handle a specific responsibility, ensuring fast response time, modularity, and easy scalability in emergency scenarios.

---

## 🌐 Frontend Architecture

### Technology
- HTML  
- CSS  
- JavaScript  

### Responsibilities
- Collect patient ID and current symptoms  
- Provide example triage scenarios  
- Send requests to the backend API  
- Display structured triage results  
- Highlight urgency level and recommended actions  

### Design Principles
- Stateless frontend  
- Minimal logic, backend-driven processing  
- Focus on clarity and fast interaction  

### Deployment
- ishosted on platforms like **Vercel**  
- Lightweight static frontend for fast load times  

---

## 🧠 Backend Architecture

### Technology
- Python  
- FastAPI  
- Uvicorn  

### Responsibilities
- Accept and validate incoming requests  
- Orchestrate the triage pipeline  
- Coordinate retrieval, pruning, and classification  
- Integrate reasoning and generate final output  
- Return structured JSON responses  

### API Design
- Primary endpoint: `POST /triage`  
- JSON-based request/response  
- Modular service-based architecture  

### Deployment
- is hosted on **Render**  
- Stateless API design for scalability  

---

## Intelligent Context Pruning Layer

### Purpose
Patient histories often contain large amounts of irrelevant or outdated data.  
This layer ensures only **clinically relevant information** is retained.

### How it Fits in the Flow
- Runs after history retrieval  
- Filters data based on current symptoms  
- Reduces input size before downstream processing  

### Benefits
- Faster processing time  
- Reduced computational overhead  
- Improved prediction accuracy  
- Lower latency for real-time use  

---

## Retrieval Layer (RAG)

### Purpose
To fetch relevant medical context from structured datasets and protocols.

### Components
- Patient history retrieval  
- Disease/protocol retrieval using vector similarity  

### Functionality
- Searches large datasets efficiently  
- Returns only context relevant to the current case  
- Supports downstream classification and reasoning  

---

## Machine Learning Layer

### Model
- Support Vector Machine (SVM)

### Responsibilities
- Analyze symptoms and filtered patient history  
- Predict possible medical conditions  
- Rank conditions based on relevance  

### Why SVM?
- Effective for structured medical data  
- Works well with limited datasets  
- Fast inference for real-time scenarios  

---

## Contextual Reasoning Layer

### Purpose
To transform predictions into meaningful, human-readable insights.

### Responsibilities
- Combine predicted condition with patient context  
- Generate explanations for the diagnosis  
- Support decision-making with contextual reasoning  

---

## Triage Generation Layer

### Responsibilities
- Assign urgency level (e.g., Immediate, Urgent)  
- Recommend immediate actions  
- Suggest next diagnostic steps  

### Output Format
- Structured JSON response  
- Designed for clarity and quick interpretation  

---

## Request–Response Flow

Below is the complete request lifecycle:

1. User enters patient ID and symptoms  
2. Frontend sends a POST request to `/triage`  
3. Backend validates input  
4. Patient history is retrieved  
5. Context pruning removes irrelevant data  
6. SVM model predicts possible conditions  
7. Relevant medical protocols are retrieved (RAG)  
8. Contextual reasoning generates explanation  
9. Triage output is structured with actions and priority  
10. Response is returned to frontend  
11. Frontend displays results clearly  

---

## Security Considerations

- No sensitive data exposed to frontend  
- API keys stored securely in environment variables  
- Backend isolated from frontend  
- Input validation to prevent malformed requests  

---

## Scalability & Performance

### Performance Focus
- Designed for **low-latency responses (<500ms target)**  
- Context pruning reduces processing time  
- Efficient retrieval minimizes overhead  

### Scalability
- Stateless backend design  
- Modular pipeline (retrieval, ML, reasoning separated)  
- Easily extendable with new datasets or models  

---

## Design Rationale

Key architectural decisions were made to:

- Prioritize **speed and relevance** in emergency scenarios  
- Reduce noise using intelligent context pruning  
- Combine ML classification with retrieval and reasoning  
- Maintain modularity for easy upgrades and experimentation  

---

## Future Architecture Extensions

The system is designed to support future enhancements such as:

- Voice-based triage input  
- Integration with hospital information systems  
- Advanced classification models (beyond SVM)  
- Real-time streaming data support  
- Improved vector search and retrieval pipelines  

---
