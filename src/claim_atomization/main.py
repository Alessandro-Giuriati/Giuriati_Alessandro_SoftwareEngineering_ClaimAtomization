import sys
from pathlib import Path

from claim_atomization.article_selector import (
    list_article_files,
    parse_article_selection,
)
from claim_atomization.input_handler import load_article_text
from claim_atomization.text_preprocessor import preprocess_text
from claim_atomization.claim_extractor import extract_claims
from claim_atomization.output_handler import build_output_path, save_claims_to_txt
from claim_atomization.metadata_handler import (
    build_harvard_reference,
    build_metadata_path,
    load_metadata_text,
)

DEFAULT_ARTICLES_DIR = "data/articles"


def process_article(article_path: str) -> None:
    """
    Run the full claim atomization pipeline for a single article.
    """
    article_text = load_article_text(article_path)
    cleaned_text = preprocess_text(article_text)
    claims = extract_claims(cleaned_text)

    source_reference = None
    try:
        metadata_path = build_metadata_path(article_path)
        metadata_text = load_metadata_text(metadata_path)
        source_reference = build_harvard_reference(metadata_text, article_path)
    except (FileNotFoundError, ValueError):
        source_reference = None

    output_path = build_output_path(article_path)
    save_claims_to_txt(claims, output_path, source_reference=source_reference)

    print(f"\nProcessing article: {Path(article_path).name}\n")
    print("Extracted claims:\n")

    for index, claim in enumerate(claims, start=1):
        print(f"{index}. {claim}")

    print(f"\nTotal claims extracted: {len(claims)}")

    if source_reference:
        print("\nSource reference:")
        print(source_reference)

    print(f"\nClaims saved to: {output_path}\n")


def prompt_article_selection(articles_dir: str = DEFAULT_ARTICLES_DIR) -> list[str]:
    """
    Interactively prompt the user to select one or more articles.
    """
    article_paths = list_article_files(articles_dir)

    print("\nAvailable articles:\n")
    for index, article_path in enumerate(article_paths, start=1):
        print(f"{index} - {Path(article_path).name}")

    print(
        "\nEnter one or more numbers, file names, or * for all articles.\n"
        "For multiple selections, separate entries with commas.\n"
    )

    selection = input("Selection: ")
    return parse_article_selection(selection, article_paths)


def main() -> None:
    try:
        if len(sys.argv) == 1:
            selected_article_paths = prompt_article_selection()
        elif len(sys.argv) == 2:
            selected_article_paths = [sys.argv[1]]
        else:
            print(
                "Usage:\n"
                "  Interactive mode:\n"
                "    PYTHONPATH=src python src/claim_atomization/main.py\n"
                "  Single-article mode:\n"
                "    PYTHONPATH=src python src/claim_atomization/main.py "
                "'article_path'"
            )
            sys.exit(1)

        for article_path in selected_article_paths:
            process_article(article_path)

    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print(f"Error: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()