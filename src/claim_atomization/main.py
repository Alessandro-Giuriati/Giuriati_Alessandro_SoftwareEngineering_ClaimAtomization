from claim_atomization.input_handler import load_article_text
from claim_atomization.text_preprocessor import preprocess_text


def main() -> None:
    article_path = "data/articles/Mac mini and Mac Studio: Apple cannot deliver certain RAM configurations.txt"

    article_text = load_article_text(article_path)
    cleaned_text = preprocess_text(article_text)

    print(cleaned_text)


if __name__ == "__main__":
    main()