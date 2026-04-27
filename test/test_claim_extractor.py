import json

import pytest

from claim_atomization.claim_extractor import extract_claims


class FakeResponse:
    def __init__(self, output_text: str):
        self.output_text = output_text


class FakeResponses:
    def __init__(self, output_text: str):
        self.output_text = output_text

    def create(self, **kwargs):
        assert kwargs["text"]["format"]["type"] == "json_schema"
        assert kwargs["text"]["format"]["strict"] is True
        return FakeResponse(self.output_text)


class FakeOpenAI:
    output_text = ""

    def __init__(self, api_key: str):
        assert api_key == "test-api-key"
        self.responses = FakeResponses(self.output_text)


def test_extract_claims_returns_claims_from_structured_json(monkeypatch):
    fake_output = {
        "claims": [
            {"text": "Apple delayed some RAM configurations."},
            {"text": "The issue affects Mac mini and Mac Studio."},
        ]
    }

    FakeOpenAI.output_text = json.dumps(fake_output)

    monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")
    monkeypatch.setattr("claim_atomization.claim_extractor.OpenAI", FakeOpenAI)

    result = extract_claims("Example article text.")

    assert result == [
        "Apple delayed some RAM configurations.",
        "The issue affects Mac mini and Mac Studio.",
    ]


def test_extract_claims_raises_if_article_text_is_empty():
    with pytest.raises(ValueError, match="Article text is empty"):
        extract_claims("   ")


def test_extract_claims_raises_if_api_key_is_missing(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(RuntimeError, match="OpenAI API key not found"):
        extract_claims("Example article text.")


def test_extract_claims_raises_if_model_returns_invalid_json(monkeypatch):
    FakeOpenAI.output_text = "This is not JSON."

    monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")
    monkeypatch.setattr("claim_atomization.claim_extractor.OpenAI", FakeOpenAI)

    with pytest.raises(ValueError, match="could not be parsed as JSON"):
        extract_claims("Example article text.")


def test_extract_claims_raises_if_model_returns_no_valid_claims(monkeypatch):
    FakeOpenAI.output_text = json.dumps({"claims": []})

    monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")
    monkeypatch.setattr("claim_atomization.claim_extractor.OpenAI", FakeOpenAI)

    with pytest.raises(ValueError, match="no valid claims"):
        extract_claims("Example article text.")