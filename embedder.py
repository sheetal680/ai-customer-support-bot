from sentence_transformers import SentenceTransformer

# Load model once (fast + cached)
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str):
    """
    Convert text into a numeric vector
    """
    return model.encode(text)
