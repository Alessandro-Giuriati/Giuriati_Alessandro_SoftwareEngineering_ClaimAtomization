from datetime import date

from claim_atomization.metadata_handler import (
    build_harvard_reference,
    build_metadata_path,
    parse_metadata,
)


def test_build_metadata_path_returns_expected_meta_path():
    article_path = "data/articles/example_article.txt"

    result = build_metadata_path(article_path)

    assert result == "data/articles_[meta]/example_article_[meta].txt"


def test_parse_metadata_reads_key_value_lines():
    metadata_text = (
        "Title: Example Article\n"
        "Author: Ben Schwan\n"
        "Source: heise online\n"
        "Date: 13 April 2026\n"
        "URL: https://www.heise.de/example\n"
        "Harvard style Reference: Example reference\n"
    )

    result = parse_metadata(metadata_text)

    assert result["title"] == "Example Article"
    assert result["author"] == "Ben Schwan"
    assert result["source"] == "heise online"
    assert result["date"] == "13 April 2026"
    assert result["url"] == "https://www.heise.de/example"
    assert result["harvard_style_reference"] == "Example reference"


def test_build_harvard_reference_uses_existing_reference_when_available():
    metadata_text = (
        "Title: Mac mini and Mac Studio: Apple cannot deliver certain RAM configurations\n"
        "Author: Ben Schwan\n"
        "Source: heise online\n"
        "Date: 13 April 2026\n"
        "URL: https://www.heise.de/en/news/Mac-mini-and-Mac-Studio-Apple-cannot-deliver-certain-RAM-configurations-11254312.html\n"
        "Harvard style Reference: Schwan, B. (2026) 'Mac mini and Mac Studio: Apple cannot deliver certain RAM configurations', "
        "heise online, 13 April. Available at: https://www.heise.de/en/news/Mac-mini-and-Mac-Studio-Apple-cannot-deliver-certain-RAM-configurations-11254312.html "
        "(Accessed: 16 April 2026).\n"
    )

    result = build_harvard_reference(
        metadata_text=metadata_text,
        article_path="data/articles/Mac mini and Mac Studio: Apple cannot deliver certain RAM configurations.txt",
        access_date=date(2026, 4, 18),
    )

    assert result == (
        "Schwan, B. (2026) 'Mac mini and Mac Studio: Apple cannot deliver certain RAM configurations', "
        "heise online, 13 April. Available at: "
        "https://www.heise.de/en/news/Mac-mini-and-Mac-Studio-Apple-cannot-deliver-certain-RAM-configurations-11254312.html "
        "(Accessed: 16 April 2026)."
    )


def test_build_harvard_reference_builds_fallback_when_existing_reference_is_missing():
    metadata_text = (
        "Title: Example Article\n"
        "Author: Ben Schwan\n"
        "Source: heise online\n"
        "Date: 13 April 2026\n"
        "URL: https://www.heise.de/example\n"
    )

    result = build_harvard_reference(
        metadata_text=metadata_text,
        article_path="data/articles/Example Article.txt",
        access_date=date(2026, 4, 18),
    )

    assert result == (
        "Ben Schwan (2026) 'Example Article', heise online, 13 April 2026. "
        "Available at: https://www.heise.de/example "
        "(Accessed: 18 April 2026)."
    )