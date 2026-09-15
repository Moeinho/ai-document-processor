from unittest.mock import patch, MagicMock
from analyzer import analyze_document


def test_analyze_document_with_mocked_response():
    fake_json = '{"summary": "Fake summary", "key_points": ["fake point"], "topics": ["fake topic"], "category": "marketing", "sentiment": "positive"}'

    mock_completion = MagicMock()
    mock_completion.choices[0].message.content = fake_json

    with patch("analyzer.client.chat.completions.create", return_value=mock_completion):
        result = analyze_document("any text, doesn't matter")

    assert result.summary == "Fake summary"
    assert result.sentiment == "positive"
