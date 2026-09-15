# AI Document Processor

A small AI-powered document analysis API built with FastAPI, Groq (OpenAI-compatible), and Pydantic structured outputs.

## What it does

Takes raw business text and returns structured analysis: summary, key points, topics, category, and sentiment. Handles empty input, unrelated input, and basic prompt injection attempts.

## Tech stack

- Python 3.14
- FastAPI
- Groq API (OpenAI-compatible SDK)
- Pydantic (structured output + validation)
- SQLite (document storage)
- pytest (with mocked LLM responses)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

GROQ_API_KEY=your_key_here


Run the server:

```bash
uvicorn main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for interactive API docs.

## Architecture

The project is split into three layers:

- `main.py` — HTTP layer (FastAPI routes, error handling)
- `analyzer.py` — AI logic (prompt construction, model call, output validation)
- `storage.py` — persistence (SQLite)

Storing and analyzing are separate steps: a document is saved once via `POST /documents`, then can be analyzed via `POST /documents/{id}/analyze` whenever needed. The result is persisted, so subsequent `GET` requests don't require another LLM call.

## API Endpoints

### Stateless analysis

POST /analyze


```json
{"text": "..."}
```

Analyzes text directly, without storing it.

### Document storage + analysis

POST /documents

Stores raw text, returns `{"id": ...}`

GET /documents/{id}

Retrieves a stored document (and its analysis, if run)

POST /documents/{id}/analyze

Analyzes a stored document and persists the result

## Example

Request:

```json
{"text": "Revenue grew 20% this quarter, driven by strong product sales."}
```

Response:

```json
{
  "summary": "...",
  "key_points": ["..."],
  "topics": ["..."],
  "category": "sales",
  "sentiment": "positive"
}
```

## Running tests

```bash
python -m pytest -v
```

Tests cover schema validation, mocked LLM responses, and the storage endpoints (using a separate test database).

## Notes

- Uses Groq instead of OpenAI directly (OpenAI-compatible API).
- System prompt handles edge cases: empty input, non-business input, and basic prompt injection attempts (treats user text as data, not instructions).