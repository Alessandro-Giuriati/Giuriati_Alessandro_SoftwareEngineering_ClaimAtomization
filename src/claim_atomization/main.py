import sys

from claim_atomization.input_handler import load_article_text
from claim_atomization.text_preprocessor import preprocess_text
from claim_atomization.claim_extractor import extract_claims
from claim_atomization.output_handler import build_output_path, save_claims_to_txt


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: PYTHONPATH=src python src/claim_atomization/main.py 'article_path'")
        sys.exit(1)

    article_path = sys.argv[1]

    article_text = load_article_text(article_path)
    cleaned_text = preprocess_text(article_text)
    claims = extract_claims(cleaned_text)

    output_path = build_output_path(article_path)
    save_claims_to_txt(claims, output_path)

    print("\nExtracted claims:\n")

    for index, claim in enumerate(claims, start=1):
        print(f"{index}. {claim}")

    print(f"\nTotal claims extracted: {len(claims)}")
    print(f"Claims saved to: {output_path}\n")


if __name__ == "__main__":
    main()