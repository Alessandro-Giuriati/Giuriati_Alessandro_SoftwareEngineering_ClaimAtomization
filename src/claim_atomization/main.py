from claim_atomization.input_handler import load_article_text
from claim_atomization.text_preprocessor import preprocess_text
from claim_atomization.claim_extractor import extract_claims
from claim_atomization.output_handler import build_output_path, save_claims_to_txt


def main() -> None:
    article_path = (
        "data/articles/"
        "Mac mini and Mac Studio: Apple cannot deliver certain RAM "
        "configurations.txt"
    )

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