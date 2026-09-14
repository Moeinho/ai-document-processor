# AI Document Processor

A small AI-powered document analysis API built with FastAPI, Groq (OpenAI-compatible),
and Pydantic structured outputs.

## What it does
Takes raw business text and returns structured analysis: summary, key points,
topics, category, and sentiment. Handles empty/unrelated input and basic
prompt injection attempts.

## Tech stack
- Python 3.14
- FastAPI
- Groq API (OpenAI-compatible SDK)
- Pydantic (structured output + validation)
- pytest (with mocked LLM responses)

## Setup
1. `python -m venv .venv && source .venv/bin/activate`
2. `pip install -r requirements.txt`
3. Create a `.env` file with `GROQ_API_KEY=your_key`
4. `uvicorn main:app --reload`
5. Visit `http://127.0.0.1:8000/docs` for interactive API docs

## Example

POST /analyze
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

## Notes
- Uses Groq instead of OpenAI directly (OpenAI-compatible API) for free-tier access.
- System prompt handles edge cases: empty input, non-business input, and 
  basic prompt injection attempts (treats user text as data, not instructions).