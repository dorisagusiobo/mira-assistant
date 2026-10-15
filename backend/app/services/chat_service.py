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

    if session_id is None:
        session = create_session(db, title=user_text[:40] or "New Chat")
        session_id = session.id
    else:
        session = get_session(db, session_id)
        if session is None:
            session = create_session(db, title=user_text[:40] or "New Chat")
            session_id = session.id

    add_message(db, session_id, "user", user_text)
    history = get_messages_for_llm(db, session_id)
    assistant_reply = generate_reply(history)
    add_message(db, session_id, "assistant", assistant_reply)

    return {
        "session_id": session_id,
        "user_message": user_text,
        "assistant_message": assistant_reply,
    }
