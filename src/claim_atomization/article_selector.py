from pathlib import Path


def list_article_files(articles_dir: str) -> list[str]:
    """
    Return the available .txt article files in the given directory.

    Args:
        articles_dir: Directory containing article files.

    Returns:
        A sorted list of article file paths.

    Raises:
        FileNotFoundError: If the directory does not exist.
        ValueError: If the path is not a directory or no .txt files are found.
    """
    path = Path(articles_dir)

    if not path.exists():
        raise FileNotFoundError(f"Articles directory not found: {articles_dir}")

    if not path.is_dir():
        raise ValueError(f"Expected a directory, but got: {articles_dir}")

    article_paths = sorted(
        [
            str(file_path)
            for file_path in path.iterdir()
            if file_path.is_file() and file_path.suffix.lower() == ".txt"
        ],
        key=lambda item: Path(item).name.casefold(),
    )

    if not article_paths:
        raise ValueError(f"No .txt article files found in: {articles_dir}")

    return article_paths


def parse_article_selection(selection: str, article_paths: list[str]) -> list[str]:
    """
    Parse a user selection of article files.

    Supported formats:
    - *                  -> all articles
    - 1,2                -> by index
    - file1.txt,file2.txt -> by exact file name

    Args:
        selection: Raw user input.
        article_paths: Available article paths.

    Returns:
        A list of selected article paths.

    Raises:
        ValueError: If the selection is empty or contains invalid entries.
    """
    if not article_paths:
        raise ValueError("No available articles to select.")

    cleaned_selection = selection.strip()

    if not cleaned_selection:
        raise ValueError("Selection cannot be empty.")

    if cleaned_selection == "*":
        return article_paths

    tokens = [token.strip() for token in cleaned_selection.split(",") if token.strip()]

    if not tokens:
        raise ValueError("Selection cannot be empty.")

    index_map = {
        str(index): article_path
        for index, article_path in enumerate(article_paths, start=1)
    }
    name_map = {Path(article_path).name: article_path for article_path in article_paths}

    selected_paths: list[str] = []
    seen_paths: set[str] = set()
    invalid_tokens: list[str] = []

    for token in tokens:
        if token in index_map:
            candidate_path = index_map[token]
        elif token in name_map:
            candidate_path = name_map[token]
        else:
            invalid_tokens.append(token)
            continue

        if candidate_path not in seen_paths:
            selected_paths.append(candidate_path)
            seen_paths.add(candidate_path)

    if invalid_tokens:
        invalid_values = ", ".join(invalid_tokens)
        raise ValueError(f"Invalid article selection: {invalid_values}")

    return selected_paths
