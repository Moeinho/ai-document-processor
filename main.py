from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from analyzer import DocumentAnalysis, analyze_document
from schema import DocumentRequest
import json
from storage import init_db, save_document, get_document, update_document_analysis

init_db()

app = FastAPI()


@app.post("/analyze", response_model=DocumentAnalysis)
def analyze_document_endpoint(request: DocumentRequest):
    try:
        return analyze_document(request.text)
    except ValidationError:
        raise HTTPException(
            status_code=502, detail="AI model returned an invalid response."
        )
    except Exception:
        raise HTTPException(
            status_code=503, detail="AI service is temporarily unavailable."
        )


# additional endpoints for document storage and analysis


@app.post("/documents")
def create_document(request: DocumentRequest):
    doc_id = save_document(request.text)
    return {"id": doc_id}


@app.get("/documents/{doc_id}")
def read_document(doc_id: int):
    document = get_document(doc_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return {
        "id": document[0],
        "text": document[1],
        "summary": document[2],
        "key_points": json.loads(document[3]) if document[3] else [],
        "topics": json.loads(document[4]) if document[4] else [],
        "category": document[5],
        "sentiment": document[6],
    }


@app.post("/documents/{doc_id}/analyze")
def analyze_stored_document(doc_id: int):
    document = get_document(doc_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")

    try:
        result = analyze_document(document[1])  # document[1] is the text field
    except ValidationError:
        raise HTTPException(
            status_code=502, detail="AI model returned an invalid response."
        )
    except Exception:
        raise HTTPException(
            status_code=503, detail="AI service is temporarily unavailable."
        )

    update_document_analysis(doc_id, result)
    return result
