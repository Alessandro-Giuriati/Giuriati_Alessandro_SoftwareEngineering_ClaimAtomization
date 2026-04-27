"""
Main entry point for the claim atomization pipeline.

Usage:
    PYTHONPATH=src python src/claim_atomization/main.py
    PYTHONPATH=src python -m claim_atomization.main
"""

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
from claim_atomization.claim_evaluator import (
    build_manual_claims_path,
    evaluate_claims,
    format_evaluation_summary,
    load_manual_claims,
)

DEFAULT_ARTICLES_DIR = "data/articles"


def process_article(article_path: str) -> tuple[int, str, str | None]:
    """
    Run the full claim atomization pipeline for a single article.

    Returns:
        A tuple containing:
        - the total number of extracted claims
        - the saved output path
        - an optional manual evaluation summary
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

    evaluation_summary = None
    manual_claims_path = build_manual_claims_path(article_path)

    if Path(manual_claims_path).exists():
        manual_claims = load_manual_claims(manual_claims_path)
        evaluation = evaluate_claims(claims, manual_claims)
        evaluation_summary = format_evaluation_summary(evaluation)

    return len(claims), output_path, evaluation_summary

def print_article_summary(
    article_path: str,
    claim_count: int,
    output_path: str,
    evaluation_summary: str | None = None,
) -> None:
    """
    Print a compact terminal summary for a processed article.
    """
    print(f"\nProcessing article: {Path(article_path).name}\n")
    print(f"Total claims extracted: {claim_count}\n")
    print(f"Claims saved to: {output_path}\n")

    if evaluation_summary:
        print(evaluation_summary)
        print()
    else:
        print("No manual claims file found. Skipping quality evaluation.\n")

def print_article_error(article_path: str, error_message: str) -> None:
    """
    Print a compact terminal error for a failed article.
    """
    print(f"\nProcessing article: {Path(article_path).name}\n")
    print(f"Error: {error_message}\n")


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
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}")
        sys.exit(1)

    success_count = 0
    failure_count = 0

    for article_path in selected_article_paths:
        try:
            claim_count, output_path, evaluation_summary = process_article(article_path)
            print_article_summary(
                article_path,
                claim_count,
                output_path,
                evaluation_summary,
            )
            success_count += 1
        except (FileNotFoundError, ValueError, RuntimeError) as exc:
            print_article_error(article_path, str(exc))
            failure_count += 1

    if failure_count > 0 and success_count == 0:
        sys.exit(1)


if __name__ == "__main__":
    main()