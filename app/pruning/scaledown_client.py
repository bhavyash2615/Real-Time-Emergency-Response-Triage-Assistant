import os
import requests
import json
import re
from dotenv import load_dotenv

load_dotenv()

SCALEDOWN_API_KEY = os.getenv("SCALEDOWN_API_KEY")
SCALEDOWN_URL = "https://api.scaledown.xyz/compress/raw"


def repair_json(text):
    """
    Attempt to repair common JSON issues from compression.
    """

    # Replace invalid tokens
    text = re.sub(r'\bNaN\b', 'null', text)
    text = re.sub(r'\bInfinity\b', 'null', text)

    # Fix trailing commas
    text = re.sub(r',\s*}', '}', text)
    text = re.sub(r',\s*]', ']', text)

    # Close unterminated quotes if needed
    if text.count('"') % 2 != 0:
        text += '"'

    return text


def compress_history(patient_history, current_emergency):

    if not isinstance(patient_history, dict):
        return patient_history

    headers = {
        "X-API-Key": SCALEDOWN_API_KEY,
        "Content-Type": "application/json"
    }

    fields_to_compress = ["labs", "medications", "procedures"]

    for field in fields_to_compress:

        if field not in patient_history:
            continue

        field_text = json.dumps(patient_history[field])

        payload = {
            "context": field_text,
            "prompt": current_emergency,
            "scaledown": {
                "rate": 0.3
            }
        }

        try:
            response = requests.post(
                SCALEDOWN_URL,
                headers=headers,
                json=payload,
                timeout=20
            )

            if response.status_code != 200:
                continue

            data = response.json()

            compressed = (
                data.get("results", {}).get("compressed_prompt")
                or data.get("compressed_prompt")
                or data.get("compressed")
                or field_text
            )

            print(f"\nCompressed field: {field}")
            print("Before:", len(field_text))
            print("After:", len(compressed))

            # convert back to JSON safely
            try:
                patient_history[field] = json.loads(compressed)
            except:
                pass

        except Exception as e:
            print("Scaledown failed for field:", field, e)

    return patient_history