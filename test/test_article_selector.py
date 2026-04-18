from pathlib import Path

import pytest

from claim_atomization.article_selector import (
    list_article_files,
    parse_article_selection,
)


def test_list_article_files_returns_sorted_txt_files(tmp_path):
    articles_dir = tmp_path / "articles"
    articles_dir.mkdir()

    (articles_dir / "b_article.txt").write_text("B", encoding="utf-8")
    (articles_dir / "a_article.txt").write_text("A", encoding="utf-8")
    (articles_dir / "notes.md").write_text("Ignore me", encoding="utf-8")

    result = list_article_files(str(articles_dir))

    assert result == [
        str(articles_dir / "a_article.txt"),
        str(articles_dir / "b_article.txt"),
    ]


def test_list_article_files_raises_if_directory_does_not_exist(tmp_path):
    missing_dir = tmp_path / "missing_articles"

    with pytest.raises(FileNotFoundError, match="Articles directory not found"):
        list_article_files(str(missing_dir))


def test_parse_article_selection_returns_all_for_star():
    article_paths = [
        "data/articles/first.txt",
        "data/articles/second.txt",
    ]

    result = parse_article_selection("*", article_paths)

    assert result == article_paths


def test_parse_article_selection_supports_numbers():
    article_paths = [
        "data/articles/first.txt",
        "data/articles/second.txt",
    ]

    result = parse_article_selection("2,1", article_paths)

    assert result == [
        "data/articles/second.txt",
        "data/articles/first.txt",
    ]


def test_parse_article_selection_supports_file_names():
    article_paths = [
        "data/articles/first.txt",
        "data/articles/second.txt",
    ]

    result = parse_article_selection("second.txt", article_paths)

    assert result == ["data/articles/second.txt"]


def test_parse_article_selection_raises_for_invalid_entry():
    article_paths = [
        "data/articles/first.txt",
        "data/articles/second.txt",
    ]

    with pytest.raises(ValueError, match="Invalid article selection"):
        parse_article_selection("3", article_paths)