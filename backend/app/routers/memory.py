from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..dependencies import get_db
from ..schemas import MemoryCreate, MemoryOut
from ..services.memory_service import get_all_memory, upsert_memory

router = APIRouter(prefix="/api/memory", tags=["memory"])


@router.post("", response_model=MemoryOut)
def save_memory(payload: MemoryCreate, db: Session = Depends(get_db)):
    return upsert_memory(db, payload.key, payload.value)


@router.get("", response_model=list[MemoryOut])
def list_memory(db: Session = Depends(get_db)):
    return get_all_memory(db)
