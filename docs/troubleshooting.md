# Troubleshooting

### 🔹 1. Server Not Starting

**Issue:** Backend fails to start or crashes on launch  

**Possible Causes:**
- Missing dependencies  
- Incorrect environment setup  
- Port already in use  

**Solution:**
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

- Ensure port `8000` is free  
- Check for errors in terminal logs  

---

### 🔹 2. API Not Responding

**Issue:** No response from `/triage` endpoint  

**Possible Causes:**
- Backend server not running  
- Incorrect API URL  
- Network/CORS issues  

**Solution:**
- Verify server is running at `http://localhost:8000`  
- Check endpoint: `POST /triage`  
- Ensure correct headers:
```json
Content-Type: application/json
```

---

### 🔹 3. Invalid Input Errors

**Issue:** API returns 400 Bad Request  

**Possible Causes:**
- Missing required fields  
- Incorrect JSON format  

**Solution:**
Ensure request body is valid:
```json
{
  "patient_id": "10021118",
  "current_issue": "airway swelling and swollen throat"
}
```

---

### 🔹 4. Patient Not Found

**Issue:** API returns patient not found error  

**Possible Causes:**
- Invalid or missing patient ID  
- Dataset not properly loaded  

**Solution:**
- Verify patient ID exists in dataset  
- Ensure data ingestion scripts have been run  

---

### 🔹 5. Slow Response Time

**Issue:** High latency in response  

**Possible Causes:**
- Large unfiltered patient history  
- Inefficient pruning  
- System resource limitations  

**Solution:**
- Optimize context pruning logic  
- Check step-wise timing (`step_times` in response)  
- Reduce dataset size for testing  

---

### 🔹 6. Inaccurate Predictions

**Issue:** Output condition does not match expectations  

**Possible Causes:**
- Limited training data for SVM  
- Weak symptom input  
- Insufficient context after pruning  

**Solution:**
- Improve training dataset quality  
- Provide more descriptive symptoms  
- Tune pruning thresholds  

---

### 🔹 7. LLM Response Issues

**Issue:** Missing or unclear explanation  

**Possible Causes:**
- Improper context passed to reasoning layer  
- Prompt construction issues  

**Solution:**
- Check context builder logic  
- Ensure relevant history and condition are passed correctly  

---

### 🔹 8. Data Not Loading Properly

**Issue:** Empty or missing patient history  

**Possible Causes:**
- Data ingestion not completed  
- Incorrect file paths  
- Database connection issues  

**Solution:**
- Run ingestion scripts:
```bash
python ingestion/ingest_mimic.py
python ingestion/ingest_diseases.py
```
- Verify data exists in `/data` directory  

---

### 🔹 9. Module Import Errors

**Issue:** Python import errors when running backend  

**Possible Causes:**
- Incorrect project structure  
- Missing `PYTHONPATH`  

**Solution:**
Run from project root:
```bash
export PYTHONPATH=.
uvicorn app.main:app --reload
```

---

### 🔹 10. High Memory Usage

**Issue:** System consumes excessive memory  

**Possible Causes:**
- Large dataset loading  
- Inefficient retrieval or embeddings  

**Solution:**
- Use smaller datasets during development  
- Optimize retrieval queries  
- Limit context size before reasoning  

---

## 💡 Debugging Tips

- Use logs to track pipeline stages  
- Monitor `latency_ms` and `step_times` in API response  
- Test each module independently (retrieval, pruning, classification)  
- Start with small inputs before scaling  

---
