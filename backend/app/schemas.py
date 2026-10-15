from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    session_id: Optional[int] = None
    message: str = Field(..., min_length=1)


class ChatResponse(BaseModel):
    session_id: int
    user_message: str
    assistant_message: str


class MessageOut(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class SessionOut(BaseModel):
    id: int
    title: str
    created_at: datetime
    messages: List[MessageOut] = []

    class Config:
        from_attributes = True


class SessionSummaryOut(BaseModel):
    id: int
    title: str
    created_at: datetime

    class Config:
        from_attributes = True


class MemoryCreate(BaseModel):
    key: str = Field(..., min_length=1)
    value: str = Field(..., min_length=1)


class MemoryOut(BaseModel):
    key: str
    value: str

    class Config:
        from_attributes = True
