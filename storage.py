import sqlite3
import json
from schema import DocumentAnalysis

DB_NAME = "documents.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            summary TEXT,
            key_points TEXT,
            topics TEXT,
            category TEXT,
            sentiment TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_document(text: str) -> int:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("INSERT INTO documents (text) VALUES (?)", (text,))
    conn.commit()
    doc_id = cursor.lastrowid
    conn.close()
    return doc_id


def get_document(doc_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def update_document_analysis(doc_id: int, analysis: DocumentAnalysis):
    conn = sqlite3.connect(DB_NAME)
    conn.execute(
        """
        UPDATE documents
        SET summary = ?, key_points = ?, topics = ?, category = ?, sentiment = ?
        WHERE id = ?
        """,
        (
            analysis.summary,
            json.dumps(analysis.key_points),
            json.dumps(analysis.topics),
            analysis.category,
            analysis.sentiment,
            doc_id,
        ),
    )
    conn.commit()
    conn.close()
