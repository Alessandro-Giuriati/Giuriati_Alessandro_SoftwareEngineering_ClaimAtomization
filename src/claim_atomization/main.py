from claim_atomization.input_handler import load_article_text


def main():
    article_path = "data/articles/Mac mini and Mac Studio: Apple cannot deliver certain RAM configurations.txt"
    article_text = load_article_text(article_path)
    print(article_text)


if __name__ == "__main__":
    main()