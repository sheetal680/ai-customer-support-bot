from pathlib import Path

FAQ_FILE = Path("data/faqs.txt")

def load_faqs():
    faqs = []
    question = None

    with open(FAQ_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("Q:"):
                question = line.replace("Q:", "").strip().lower()
            elif line.startswith("A:") and question:
                answer = line.replace("A:", "").strip()
                faqs.append({"question": question, "answer": answer})
                question = None

    return faqs
