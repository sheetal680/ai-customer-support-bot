import os
from dotenv import load_dotenv
from groq import Groq

# FORCE load .env before anything else
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not found. Check your .env file.")

client = Groq(api_key=GROQ_API_KEY)

def generate_answer(context, question, business_name="", tone="Friendly"):
    prompt = f"""
You are a {tone.lower()} customer support assistant for {business_name or "this business"}.

Use ONLY the FAQ below to answer.
If the answer is not present, say:
"I'm not fully sure. Please contact our support team."

FAQ:
{context}

User Question:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()
