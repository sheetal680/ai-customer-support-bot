import os
from groq import Groq
import streamlit as st

def get_groq_client():
    """
    Returns a Groq client using Streamlit secrets (cloud)
    or environment variables (local fallback).
    """
    api_key = None

    # Streamlit Cloud
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]

    # Local fallback
    elif os.getenv("GROQ_API_KEY"):
        api_key = os.getenv("GROQ_API_KEY")

    else:
        raise RuntimeError("GROQ_API_KEY is not set")

    return Groq(api_key=api_key)


def generate_answer(context, question, business_name, tone):
    client = get_groq_client()

    prompt = f"""
You are a professional customer support assistant for {business_name}.
Tone: {tone}

Answer clearly and professionally using ONLY the FAQ below.
Do not hallucinate.

FAQ:
{context}

User Question:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()
