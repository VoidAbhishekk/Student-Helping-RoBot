# -------------------------------
# COMMON TEXT HELPERS
# -------------------------------
HEADER ="━━━━━━━━━━━━━━━━━━━━━━\n\n"
FOOTER = "\n\n━━━━━━━━━━━━━━━━━━━━━━\n"


def format_message(text: str) -> str:
    """
    Adds the common footer to every bot message.
    """
    return f"{text}{FOOTER}"