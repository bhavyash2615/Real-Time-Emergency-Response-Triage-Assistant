from openai import OpenAI

from app.config import GROQ_API_KEY

client = OpenAI(
    api_key="YOUR_GROQ_API_KEY",
    base_url="https://api.groq.com/openai/v1"
)
print("GROQ KEY:", GROQ_API_KEY[:10])

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": "hello"}]
)

print(response.choices[0].message.content)