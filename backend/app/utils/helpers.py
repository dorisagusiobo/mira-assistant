def truncate_text(text: str, max_length: int = 80) -> str:
    text = text.strip()
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."
