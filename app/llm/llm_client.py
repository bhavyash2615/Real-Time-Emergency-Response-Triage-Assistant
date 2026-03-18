import time
from google import genai
from openai import OpenAI

from app.config import (
    GEMINI_API_KEY,
    GROQ_API_KEY,
    PRIMARY_LLM_MODEL,
    BACKUP_LLM_MODEL
)

# ---------------- CLIENTS ----------------

# Gemini client (Primary)
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

# Groq client (Backup)
groq_client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
    timeout=3,
)


def generate_triage(patient_history: str, current_emergency: str) -> dict:
    """
    Calls primary LLM (Gemini).
    If failure occurs → retry once → fallback to Groq.
    """

    prompt = f"""
You are an emergency medical triage assistant supporting healthcare professionals.

Patient Current Emergency:
{current_emergency}

Relevant Patient History:
{patient_history}

Instructions:
1. Identify the most likely medical condition.
2. Assign a triage urgency level (LOW, MEDIUM, HIGH, CRITICAL).
3. Recommend immediate next actions.
4. Mention which parts of the history influenced your decision.
5. If uncertain, say so clearly.

Respond in structured format.
"""

    # ---------------- PRIMARY MODEL (Gemini) ----------------
    try:

        response = gemini_client.models.generate_content(
            model=PRIMARY_LLM_MODEL,
            contents=prompt
        )

        return {
            "recommendation": response.text
        }

    except Exception as e:

        print("Gemini failed:", e)

        # ---------------- RETRY ----------------
        try:

            print("Retrying Gemini in 1 second...")
            time.sleep(1)

            response = gemini_client.models.generate_content(
                model=PRIMARY_LLM_MODEL,
                contents=prompt
            )

            return {
                "recommendation": response.text
            }

        except Exception as e2:

            print("Retry failed. Switching to Groq backup:", e2)

            # ---------------- BACKUP MODEL (Groq) ----------------

            response = groq_client.chat.completions.create(
                model=BACKUP_LLM_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )

            return {
                "recommendation": response.choices[0].message.content
            }