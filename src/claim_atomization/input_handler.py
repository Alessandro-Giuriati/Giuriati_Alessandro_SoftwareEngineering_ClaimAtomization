from pathlib import Path


def load_article_text(file_path: str) -> str:
    """
    Load and validate a local article stored as a .txt file.

    Args:
        file_path: Path to the article file.

    Returns:
        The article content as a string.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the path is not a file, the extension is not .txt,
                    or the file is empty.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Article file not found: {file_path}")

    if not path.is_file():
        raise ValueError(f"Expected a file, but got: {file_path}")

    if path.suffix.lower() != ".txt":
        raise ValueError(
            f"Invalid file type for article input: {path.suffix}. Expected .txt"
        )

    article_text = path.read_text(encoding="utf-8").strip()

    if not article_text:
        raise ValueError(f"The article file is empty: {file_path}")

    return article_text
