import pytest
from schema import DocumentAnalysis, DocumentRequest
from pydantic import ValidationError


def test_valid_document_analysis():
    data = {
        "summary": "Test summary",
        "key_points": ["point 1"],
        "topics": ["topic 1"],
        "category": "marketing",
        "sentiment": "positive",
    }
    result = DocumentAnalysis(**data)
    assert result.sentiment == "positive"


def test_invalid_sentiment_rejected():
    data = {
        "summary": "Test",
        "key_points": [],
        "topics": [],
        "category": "marketing",
        "sentiment": "very happy",
    }
    with pytest.raises(ValidationError):
        DocumentAnalysis(**data)


def test_document_request_requires_text():
    with pytest.raises(ValidationError):
        DocumentRequest()  # without text should raise ValidationError
