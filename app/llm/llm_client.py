import time
import concurrent.futures
from google import genai
from openai import OpenAI

from app.config import (
    GEMINI_API_KEY,
    GROQ_API_KEY,
    PRIMARY_LLM_MODEL,
    BACKUP_LLM_MODEL
)

# ---------------- CLIENTS ----------------

# Groq client (Primary)
groq_client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
    timeout=3,
)

# Gemini client (Backup)
gemini_client = genai.Client(api_key=GEMINI_API_KEY)


# ---------------- RESPONSE NORMALIZER ----------------

def extract_text(response, provider: str) -> str:
    if provider == "groq":
        return response.choices[0].message.content
    elif provider == "gemini":
        return response.text
    return ""


def generate_triage(context: str) -> dict:

    if len(context) > 400:
        context = context[:400]

    prompt = f"""
{context}

Explain in 3 short sentences why symptoms match the condition.

"""

    def call_groq_with_timeout():
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(
                lambda: groq_client.chat.completions.create(
                    model=PRIMARY_LLM_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2
                )
            )
            return future.result(timeout=2.5)

    # ---------------- PRIMARY TRY ----------------
    try:
        response = call_groq_with_timeout()
        return {"recommendation": extract_text(response, "groq")}

    except Exception as e:
        print("Groq failed:", e)

    # ---------------- RETRY ----------------
    try:
        print("Retrying Groq in 0.2s...")
        time.sleep(0.2)

        response = call_groq_with_timeout()
        return {"recommendation": extract_text(response, "groq")}

    except Exception as e2:
        print("Retry failed. Switching to Gemini:", e2)

    # ---------------- BACKUP ----------------
    try:
        response = gemini_client.models.generate_content(
            model=BACKUP_LLM_MODEL,
            contents=prompt,
            generation_config={
                "max_output_tokens": 50,
                "temperature": 0.2,
                "top_p": 0.8,
                "stop_sequences": ["\n\n"]
            }
        )

        return {"recommendation": extract_text(response, "gemini")}

    except Exception as e3:
        print("Gemini also failed:", e3)
        return {"recommendation": "Service temporarily unavailable."}