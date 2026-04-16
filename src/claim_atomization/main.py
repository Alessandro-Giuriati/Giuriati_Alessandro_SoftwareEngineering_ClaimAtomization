from claim_atomization.input_handler import load_article_text
from claim_atomization.text_preprocessor import preprocess_text
from claim_atomization.claim_extractor import extract_claims


def main() -> None:
    article_path = "data/articles/Mac mini and Mac Studio: Apple cannot deliver certain RAM configurations.txt"
    
    article_text = load_article_text(article_path)
    cleaned_text = preprocess_text(article_text)
    claims = extract_claims(cleaned_text)

    print("\nExtracted claims:\n")

    for index, claim in enumerate(claims, start=1):
        print(f"{index}. {claim}")

    print(f"\nTotal claims extracted: {len(claims)}\n")


if __name__ == "__main__":
    main()