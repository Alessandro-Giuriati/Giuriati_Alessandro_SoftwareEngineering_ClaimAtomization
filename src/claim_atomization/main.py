import sys

from claim_atomization.input_handler import load_article_text
from claim_atomization.text_preprocessor import preprocess_text
from claim_atomization.claim_extractor import extract_claims
from claim_atomization.output_handler import build_output_path, save_claims_to_txt
from claim_atomization.metadata_handler import (
    build_harvard_reference,
    build_metadata_path,
    load_metadata_text,
)


def main() -> None:
    if len(sys.argv) != 2:
        print(
            "Usage: PYTHONPATH=src python src/claim_atomization/main.py "
            "'article_path'"
        )
        sys.exit(1)

    article_path = sys.argv[1]

    try:
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

        print("\nExtracted claims:\n")

        for index, claim in enumerate(claims, start=1):
            print(f"{index}. {claim}")

        print(f"\nTotal claims extracted: {len(claims)}")

        if source_reference:
            print("\nSource reference:")
            print(source_reference)

        print(f"\nClaims saved to: {output_path}\n")

    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print(f"Error: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()