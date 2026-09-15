# -------------------------------
# COMMON TEXT HELPERS
# -------------------------------

FOOTER = "\n\n━━━━━━━━━━━━━━━━━━━━━━\nMade with ❤️ by Abhishek\n(@VoidAbhishekk)"


def format_message(text: str) -> str:
    """
    Adds the common footer to every bot message.
    """
    return f"{text}{FOOTER}"