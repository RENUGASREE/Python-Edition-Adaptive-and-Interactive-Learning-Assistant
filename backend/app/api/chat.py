from fastapi import APIRouter
from .. import schemas

router = APIRouter()

@router.post("/query", response_model=schemas.ChatResponse)
def chat_query(req: schemas.ChatRequest):
    # Placeholder: implement RAG retrieval + LLM synthesis here
    answer = f"(stub) I received your question: {req.query}. This will be answered by RAG in later iterations."
    sources = ["lesson_01.md"]
    return {"answer": answer, "sources": sources}
