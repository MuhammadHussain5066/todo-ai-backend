from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)

    conversation_id: int = Field(index=True)

    role: str  # "user" | "assistant"
    content: str

    created_at: datetime = Field(default_factory=datetime.utcnow)
