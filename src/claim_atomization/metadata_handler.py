from datetime import date
from pathlib import Path
import re


def build_metadata_path(article_path: str) -> str:
    """
    Build the expected metadata file path associated with an article file.

    Example:
    data/articles/example_article.txt
    -> data/articles_[meta]/example_article_[meta].txt
    """
    article = Path(article_path)
    metadata_dir = article.parent.parent / f"{article.parent.name}_[meta]"
    metadata_filename = f"{article.stem}_[meta]{article.suffix}"

    return str(metadata_dir / metadata_filename)


def load_metadata_text(metadata_path: str) -> str:
    """
    Load a metadata text file.

    Raises:
        FileNotFoundError: If the metadata file does not exist.
        ValueError: If the file is empty.
    """
    path = Path(metadata_path)

    if not path.exists():
        raise FileNotFoundError(f"Metadata file not found: {metadata_path}")

    if not path.is_file():
        raise ValueError(f"Expected a metadata file, but got: {metadata_path}")

    metadata_text = path.read_text(encoding="utf-8").strip()

    if not metadata_text:
        raise ValueError(f"The metadata file is empty: {metadata_path}")

    return metadata_text


def parse_metadata(metadata_text: str) -> dict[str, str]:
    """
    Parse metadata from key-value lines such as:

    Title: ...
    Author: ...
    Source: ...
    Date: ...
    URL: ...
    Harvard style Reference: ...

    Returns:
        A dictionary with normalized keys.
    """
    metadata: dict[str, str] = {}
    lines = [line.strip() for line in metadata_text.splitlines() if line.strip()]

    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            normalized_key = key.strip().lower().replace(" ", "_")
            metadata[normalized_key] = value.strip()

    return metadata


def extract_year(raw_value: str | None) -> str:
    """
    Extract a four-digit year from a date-like string.
    """
    if not raw_value:
        return "n.d."

    match = re.search(r"\b(19|20)\d{2}\b", raw_value)
    if match:
        return match.group(0)

    return "n.d."


def build_harvard_reference(metadata_text: str, article_path: str, access_date: date | None = None,) -> str:
    """
    Build a Harvard-style source reference from metadata.

    Priority:
    1. Use the pre-written Harvard-style reference if available.
    2. Otherwise, build a simple fallback reference from available fields.
    """
    metadata = parse_metadata(metadata_text)

    existing_reference = metadata.get("harvard_style_reference")
    if existing_reference:
        return existing_reference

    article_title = Path(article_path).stem
    title = metadata.get("title", article_title)
    author = metadata.get("author") or metadata.get("source")
    source = metadata.get("source")
    raw_date = metadata.get("date")
    year = extract_year(raw_date)
    url = metadata.get("url")

    if not url:
        raise ValueError("Metadata does not contain a usable URL.")

    if access_date is None:
        access_date = date.today()

    formatted_access_date = access_date.strftime("%d %B %Y")

    if author and source and raw_date:
        return (
            f"{author} ({year}) '{title}', {source}, {raw_date}. "
            f"Available at: {url} "
            f"(Accessed: {formatted_access_date})."
        )

    if author:
        return (
            f"{author} ({year}) {title}. "
            f"Available at: {url} "
            f"(Accessed: {formatted_access_date})."
        )

    return (
        f"{title} ({year}) "
        f"Available at: {url} "
        f"(Accessed: {formatted_access_date})."
    )