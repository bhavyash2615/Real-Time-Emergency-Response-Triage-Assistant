from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Data paths
PATIENT_DATA_PATH = BASE_DIR / "data" / "patients"
DISEASE_DATA_PATH = BASE_DIR / "data" / "diseases"

# Vector DB storage
VECTOR_DB_PATH = BASE_DIR / "vector_db_store"

# Embedding model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Retrieval settings
TOP_K_PROTOCOLS = 5
TOP_K_HISTORY = 3

# Token optimization
MAX_CONTEXT_TOKENS = 800

# LLM settings
PRIMARY_LLM_MODEL = "llama-3.1-8b-instant"
BACKUP_LLM_MODEL = "gemini-2.5-flash"
TEMPERATURE = 0.2

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")