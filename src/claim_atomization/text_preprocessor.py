import re


def preprocess_text(article_text: str) -> str:
    """
    Clean article text while preserving its meaning.

    This function performs only basic normalization:
    - removes leading and trailing whitespace
    - normalizes line breaks
    - removes extra spaces inside lines
    - collapses multiple empty lines into a single empty line

    Args:
        article_text: Raw article text.

    Returns:
        A cleaned version of the article text.
    """
    cleaned_text = article_text.replace("\r\n", "\n").replace("\r", "\n")
    cleaned_text = cleaned_text.strip()

    lines = cleaned_text.split("\n")
    normalized_lines = []

    for line in lines:
        normalized_line = re.sub(r"\s+", " ", line).strip()
        normalized_lines.append(normalized_line)

    cleaned_text = "\n".join(normalized_lines)
    cleaned_text = re.sub(r"\n{3,}", "\n\n", cleaned_text)

    return cleaned_text