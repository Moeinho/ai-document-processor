from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from analyzer import DocumentAnalysis, analyze_document
from schema import DocumentRequest

app = FastAPI()


@app.post("/analyze", response_model=DocumentAnalysis)
def analyze_document_endpoint(request: DocumentRequest):
    try:
        return analyze_document(request.text)
    except ValidationError:
        raise HTTPException(
            status_code=502,
            detail="AI model returned an invalid response."
        )
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="AI service is temporarily unavailable."
        )
