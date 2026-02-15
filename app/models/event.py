from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class TaskEvent(SQLModel, table=True):
    __tablename__ = "task_events"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int
    event_type: str  # created, updated, completed, deleted
    user_id: Optional[str] = None
    old_data: Optional[str] = None  # JSON
    new_data: Optional[str] = None  # JSON
    timestamp: datetime = Field(default_factory=datetime.utcnow)
