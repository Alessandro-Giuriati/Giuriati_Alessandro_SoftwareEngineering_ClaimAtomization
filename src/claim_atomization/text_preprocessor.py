import re


def preprocess_text(article_text: str) -> str:
    """
    Clean article text while preserving its structure.

    This function performs conservative normalization:
    - normalizes line endings
    - removes trailing whitespace from each line
    - preserves paragraph breaks and line structure
    - collapses excessive blank lines into a maximum of two
    - rejects empty input after cleaning

    Args:
        article_text: Raw article text.

    Returns:
        A cleaned version of the article text.

    Raises:
        ValueError: If the article text is empty after preprocessing.
    """
    cleaned_text = article_text.replace("\r\n", "\n").replace("\r", "\n")

    lines = cleaned_text.split("\n")
    normalized_lines = [line.rstrip() for line in lines]

    cleaned_text = "\n".join(normalized_lines).strip()
    cleaned_text = re.sub(r"\n{3,}", "\n\n", cleaned_text)

    if not cleaned_text:
        raise ValueError("Article text is empty after preprocessing.")

    return cleaned_text
