from sqlalchemy.orm import Session
from ..models import UserMemory


def upsert_memory(db: Session, key: str, value: str):
    memory = db.query(UserMemory).filter(UserMemory.key == key).first()
    if memory:
        memory.value = value
    else:
        memory = UserMemory(key=key, value=value)
        db.add(memory)

    db.commit()
    db.refresh(memory)
    return memory


def get_all_memory(db: Session):
    return db.query(UserMemory).order_by(UserMemory.created_at.desc()).all()
