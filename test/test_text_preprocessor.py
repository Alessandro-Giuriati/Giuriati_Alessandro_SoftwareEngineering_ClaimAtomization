from claim_atomization.text_preprocessor import preprocess_text


def test_preprocess_text_normalizes_line_breaks():
    raw_text = "Line 1\r\nLine 2\rLine 3"

    result = preprocess_text(raw_text)

    assert result == "Line 1\nLine 2\nLine 3"


def test_preprocess_text_removes_extra_spaces_inside_lines():
    raw_text = "This   is   a    test"

    result = preprocess_text(raw_text)

    assert result == "This is a test"


def test_preprocess_text_strips_leading_and_trailing_whitespace():
    raw_text = "   Hello world   "

    result = preprocess_text(raw_text)

    assert result == "Hello world"


def test_preprocess_text_collapses_multiple_empty_lines():
    raw_text = "Line 1\n\n\n\nLine 2"

    result = preprocess_text(raw_text)

    assert result == "Line 1\n\nLine 2"


def test_preprocess_text_handles_mixed_noise_together():
    raw_text = "  First   line \r\n\r\n\r\n Second    line   "

    result = preprocess_text(raw_text)

    assert result == "First line\n\nSecond line"