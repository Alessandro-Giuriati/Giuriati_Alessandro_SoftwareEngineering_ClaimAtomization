import pytest

from claim_atomization.text_preprocessor import preprocess_text


def test_preprocess_text_normalizes_line_breaks():
    raw_text = "Line 1\r\nLine 2\rLine 3"

    result = preprocess_text(raw_text)

    assert result == "Line 1\nLine 2\nLine 3"


def test_preprocess_text_preserves_extra_spaces_inside_lines():
    raw_text = "This   is   a    test"

    result = preprocess_text(raw_text)

    assert result == "This   is   a    test"


def test_preprocess_text_preserves_leading_indentation_inside_lines():
    raw_text = "Title\n    Indented paragraph"

    result = preprocess_text(raw_text)

    assert result == "Title\n    Indented paragraph"


def test_preprocess_text_removes_trailing_whitespace():
    raw_text = "Line 1   \nLine 2\t"

    result = preprocess_text(raw_text)

    assert result == "Line 1\nLine 2"


def test_preprocess_text_strips_outer_document_whitespace():
    raw_text = "   \nHello world\n   "

    result = preprocess_text(raw_text)

    assert result == "Hello world"


def test_preprocess_text_collapses_excessive_empty_lines():
    raw_text = "Line 1\n\n\n\nLine 2"

    result = preprocess_text(raw_text)

    assert result == "Line 1\n\nLine 2"


def test_preprocess_text_preserves_paragraph_structure_with_mixed_noise():
    raw_text = "  First   line \r\n\r\n\r\n Second    line   "

    result = preprocess_text(raw_text)

    assert result == "First   line\n\n Second    line"


def test_preprocess_text_raises_if_text_is_empty_after_cleaning():
    with pytest.raises(ValueError, match="empty"):
        preprocess_text("   \n\t   ")