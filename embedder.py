import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def get_embedding(text: str):
    """
    Generates vector embedding using Groq
    """
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding
