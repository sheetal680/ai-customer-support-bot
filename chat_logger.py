import csv
import os
from datetime import datetime

LOG_FILE = "logs/conversations.csv"

def log_conversation(question, matched_faq, answer):
    os.makedirs("logs", exist_ok=True)
    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "question",
                "matched_faq",
                "answer"
            ])

        writer.writerow([
            datetime.now().isoformat(),
            question,
            matched_faq,
            answer
        ])
