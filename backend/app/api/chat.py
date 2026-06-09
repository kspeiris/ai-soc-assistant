from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, dependencies
from ..services.llm_analyzer import chat_assistant
from ..services.rag_service import retrieve_context
from ..database import get_db

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/")
def chat(request: schemas.ChatRequest, db: Session = Depends(get_db), current_user = Depends(dependencies.get_current_user)):
    # Optionally use RAG context
    context = retrieve_context(request.message) if request.context is None else request.context
    answer = chat_assistant(request.message, context)
    return {"response": answer}