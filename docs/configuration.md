# Configuration

This document describes the configuration options required to run
**Real-Time-Emergency-Response-Triage-Assistant** in both local and production environments.

Configuration is managed using **environment variables** to ensure
security and flexibility across deployments.

---
## 🔐 Environment Variables

The backend requires the following environment variables to function correctly.

### Required Variables

| Variable Name | Description |
|---------------|-------------|
| `GROQ_API_KEY` | API key used to access the Large Language Model |
| `GEMINI_API_KEY` |BACKUP LLM |

---
### 📁 Configuration File (.env)

For local development, create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```
**Do not commit the .env file to version control.**

---
### 🖥️ Local Development Configuration
**Backend**
- Reads environment variables from .env
- uvicorn app.main:app --reload
- Runs on http://localhost:8000/docs then POST/Triage
- Debug mode disabled by default
**Frontend**
- Uses a hardcoded backend URL during development
- Can be updated in script.js if needed

---

### ☁️ Production Configuration
**Backend (Render)**
- Environment variables are configured in the Render dashboard
- Backend URL is exposed publicly
- Auto-redeploy triggered on GitHub updates
**Frontend (Vercel)**
- No environment variables required
- Only static files are deployed
- Backend API URL points to Render deployment

---

### 🔁 Switching Between Environments
To switch between local and production environments:
- Update backend API URL in script.js
- Restart the backend server
- Ensure correct environment variables are set

---

### ⚙️ Optional Configuration Parameters
Some internal parameters can be adjusted directly in the backend code:
- latency measurement
- Maximum token limits
- LLM temperature and model choice
- These parameters are intentionally kept internal to prevent misuse.

---

### 🔒 Security Best Practices
- Never expose API keys in frontend code
- Use environment variables for all secrets
- Avoid logging sensitive values
- Restrict API access to backend only
