from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies import get_db
from ..schemas import ChatRequest, ChatResponse
from ..services.chat_service import handle_chat
from ..services.llm_service import LLMUnavailableError
from ..utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def chat(payload: ChatRequest, db: Session = Depends(get_db)):
    try:
        return handle_chat(db, payload.session_id, payload.message)
    except LLMUnavailableError as error:
        logger.warning("Chat reply failed: %s", error)
        raise HTTPException(
            status_code=502,
            detail="Mira couldn't reach the AI service. Please try again in a moment.",
        ) from error
