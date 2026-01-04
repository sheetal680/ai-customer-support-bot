BANNED_WORDS = ["abuse", "hate", "sex", "violence", "kill", "attack", "terror"]

def is_safe(text: str) -> bool:
    if not text:
        return False
    text = text.lower()
    return not any(word in text for word in BANNED_WORDS)
