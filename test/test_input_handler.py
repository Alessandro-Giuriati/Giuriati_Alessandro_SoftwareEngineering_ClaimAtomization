from pathlib import Path

import pytest

from claim_atomization.input_handler import load_article_text


def test_load_article_text_returns_content_for_valid_txt_file(tmp_path):
    article = tmp_path / "article.txt"
    article.write_text("Hello world", encoding="utf-8")

    result = load_article_text(str(article))

    assert result == "Hello world"


def test_load_article_text_raises_if_file_does_not_exist(tmp_path):
    missing_file = tmp_path / "missing.txt"

    with pytest.raises(FileNotFoundError, match="Article file not found"):
        load_article_text(str(missing_file))


def test_load_article_text_raises_if_path_is_not_a_file(tmp_path):
    directory = tmp_path / "folder"
    directory.mkdir()

    with pytest.raises(ValueError, match="Expected a file"):
        load_article_text(str(directory))


def test_load_article_text_raises_if_extension_is_not_txt(tmp_path):
    article = tmp_path / "article.md"
    article.write_text("content", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid file type"):
        load_article_text(str(article))


def test_load_article_text_raises_if_file_is_empty(tmp_path):
    article = tmp_path / "empty.txt"
    article.write_text("   \n   ", encoding="utf-8")

    with pytest.raises(ValueError, match="empty"):
        load_article_text(str(article))