from pydantic import BaseModel
from typing import Literal


class DocumentAnalysis(BaseModel):
    summary: str
    key_points: list[str]
    topics: list[str]
    category: str
    sentiment: Literal["positive", "negative", "neutral"]


class DocumentRequest(BaseModel):
    text: str
