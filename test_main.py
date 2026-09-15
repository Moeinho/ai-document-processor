import os

os.environ.setdefault("TESTING", "1")

import storage

storage.DB_NAME = "test_documents.db"
storage.init_db()

from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)


def test_create_and_get_document():
    response = client.post("/documents", json={"text": "Some business text"})
    assert response.status_code == 200
    doc_id = response.json()["id"]

    get_response = client.get(f"/documents/{doc_id}")
    assert get_response.status_code == 200


def test_analyze_stored_document():
    response = client.post(
        "/documents", json={"text": "Revenue grew 20% this quarter."}
    )
    doc_id = response.json()["id"]

    fake_json = '{"summary": "Revenue increased by 20% this quarter.", "key_points": ["Revenue growth", "Quarterly performance"], "topics": ["finance", "business"], "category": "finance", "sentiment": "positive"}'
    mock_completion = MagicMock()
    mock_completion.choices[0].message.content = fake_json

    with patch("analyzer.client.chat.completions.create", return_value=mock_completion):
        analyze_response = client.post(f"/documents/{doc_id}/analyze")

    assert analyze_response.status_code == 200
    assert (
        analyze_response.json()["summary"] == "Revenue increased by 20% this quarter."
    )
    assert analyze_response.json()["sentiment"] == "positive"
    assert analyze_response.json()["key_points"] == [
        "Revenue growth",
        "Quarterly performance",
    ]

    get_response = client.get(f"/documents/{doc_id}")
    assert get_response.json()["summary"] == "Revenue increased by 20% this quarter."
