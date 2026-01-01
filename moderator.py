# moderator.py
# Free, rule-based safety layer (no APIs, no cost)

BANNED_WORDS = [
    "abuse",
    "hate",
    "sex",
    "violence",
    "kill",
    "attack",
    "terror",
]

def is_safe(text: str) -> bool:
    """
    Returns False if the input contains unsafe or abusive content.
    """
    if not text:
        return False

    text = text.lower()
    return not any(word in text for word in BANNED_WORDS)
