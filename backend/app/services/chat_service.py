from sqlalchemy.orm import Session
from ..models import ChatMessage, ChatSession
from .llm_service import generate_reply


def create_session(db: Session, title: str = "New Chat") -> ChatSession:
    session = ChatSession(title=title)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_session(db: Session, session_id: int):
    return db.query(ChatSession).filter(ChatSession.id == session_id).first()


def add_message(db: Session, session_id: int, role: str, content: str) -> ChatMessage:
    message = ChatMessage(session_id=session_id, role=role, content=content)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_messages_for_llm(db: Session, session_id: int) -> list[dict]:
    messages = (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )
    return [{"role": msg.role, "content": msg.content} for msg in messages]


def handle_chat(db: Session, session_id: int | None, user_text: str) -> dict:
    user_text = user_text.strip()
    session = get_session(db, session_id) if session_id is not None else None
    history = get_messages_for_llm(db, session.id) if session else []

    # Ask the AI first and save only once it answers, so a failed request
    # never leaves an unanswered or duplicated message in the conversation.
    assistant_reply = generate_reply([*history, {"role": "user", "content": user_text}])

    if session is None:
        session = create_session(db, title=user_text[:40] or "New Chat")
    add_message(db, session.id, "user", user_text)
    add_message(db, session.id, "assistant", assistant_reply)

    return {
        "session_id": session.id,
        "user_message": user_text,
        "assistant_message": assistant_reply,
    }
