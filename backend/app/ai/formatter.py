import re


def clean_response(text: str) -> str:
    """
    Clean AI response and improve formatting.
    """

    if not text:
        return ""

    text = text.strip()

    # Remove duplicate blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Normalize bullets
    text = text.replace("•", "-")
    text = text.replace("* ", "- ")

    # Remove extra spaces
    text = re.sub(r"[ \t]+", " ", text)

    return text