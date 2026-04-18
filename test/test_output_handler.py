import pytest

from claim_atomization.output_handler import (
    build_output_path,
    format_claims_as_text,
    save_claims_to_txt,
)


def test_format_claims_as_text_returns_numbered_output():
    claims = ["Claim one.", "Claim two."]

    result = format_claims_as_text(claims)

    assert "Extracted claims:" in result
    assert "1. Claim one." in result
    assert "2. Claim two." in result
    assert "Total claims extracted: 2" in result


def test_format_claims_as_text_raises_if_claims_are_empty():
    with pytest.raises(ValueError, match="No claims available"):
        format_claims_as_text([])


def test_build_output_path_returns_sanitized_output_path():
    article_path = "data/articles/My Article!!!.txt"

    result = build_output_path(article_path)

    assert result == "data/output/my_article_claims.txt"


def test_build_output_path_raises_if_safe_name_is_empty():
    with pytest.raises(ValueError, match="Could not derive"):
        build_output_path("data/articles/@@@.txt")


def test_save_claims_to_txt_creates_file_and_writes_content(tmp_path):
    output_file = tmp_path / "results" / "claims.txt"
    claims = ["Claim one.", "Claim two."]

    save_claims_to_txt(claims, str(output_file))

    assert output_file.exists()

    content = output_file.read_text(encoding="utf-8")
    assert "Extracted claims:" in content
    assert "1. Claim one." in content
    assert "2. Claim two." in content
    assert "Total claims extracted: 2" in content


def test_save_claims_to_txt_raises_if_output_path_is_empty():
    with pytest.raises(ValueError, match="Output path cannot be empty"):
        save_claims_to_txt(["Claim one."], "")