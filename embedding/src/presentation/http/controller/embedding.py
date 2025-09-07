from typing import List

from fastapi import APIRouter
from pydantic import BaseModel
from src.application.service.embedding import encode

router = APIRouter()


class Embedding(BaseModel):
    sentences: List[str]


@router.post("/embedding")
async def embedding(embedding: Embedding):
    return {
        "code": 200,
        "error": "",
        "message": "",
        "data": encode(embedding.sentences).tolist(),
    }
