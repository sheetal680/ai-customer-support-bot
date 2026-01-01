from embedder import get_embedding

def load_faqs(path="data/faqs.txt"):
    """
    Loads FAQ blocks from a text file.
    Each FAQ is separated by a blank line.
    """
    with open(path, "r", encoding="utf-8") as f:
        return [
            block.strip()
            for block in f.read().split("\n\n")
            if block.strip()
        ]

def build_faq_vectors(faqs):
    """
    Converts FAQs into vector embeddings.
    """
    return [get_embedding(faq) for faq in faqs]
