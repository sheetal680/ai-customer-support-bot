import os
from groq import Groq, GroqError


def generate_answer(best_faq, user_question, business_name, tone):
    """
    Hardened Groq integration.
    This function will NEVER crash the Streamlit app.
    """

    api_key = os.getenv("GROQ_API_KEY")

    # 1️⃣ Absolute guard: no key
    if not api_key or not api_key.startswith("gsk_"):
        return (
            "Our AI service is temporarily unavailable. "
            "Please contact our support team for assistance."
        )

    system_prompt = f"""
You are a professional customer support agent for {business_name}.
Tone: {tone}.
Answer clearly and politely using ONLY the provided FAQ.
"""

    user_prompt = f"""
FAQ:
{best_faq}

Customer Question:
{user_question}
"""

    try:
        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.4,
            max_tokens=300,
        )

        return response.choices[0].message.content.strip()

    except GroqError:
        return (
            "I’m unable to retrieve that information right now. "
            "Please contact our support team for accurate assistance."
        )

    except Exception:
        return (
            "Something went wrong on our side. "
            "Please contact our support team for assistance."
        )
