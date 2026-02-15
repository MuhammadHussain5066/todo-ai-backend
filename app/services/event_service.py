from sqlalchemy.ext.asyncio import AsyncSession
from app.models.event import TaskEvent
from sqlalchemy import select
import json
from typing import Optional

async def log_event(
    session: AsyncSession,
    task_id: int,
    event_type: str,
    user_id: Optional[str] = None,
    old_data: Optional[dict] = None,
    new_data: Optional[dict] = None
):
    """Log task events for audit trail"""
    event = TaskEvent(
        task_id=task_id,
        event_type=event_type,
        user_id=user_id,
        old_data=json.dumps(old_data) if old_data else None,
        new_data=json.dumps(new_data) if new_data else None
    )
    session.add(event)
    await session.commit()
    return event

async def get_task_history(session: AsyncSession, task_id: int):
    """Get all events for a specific task"""
    result = await session.execute(
        select(TaskEvent).where(TaskEvent.task_id == task_id).order_by(TaskEvent.timestamp.desc())
    )
    return result.scalars().all()

async def get_recent_events(session: AsyncSession, limit: int = 50):
    """Get recent events across all tasks"""
    result = await session.execute(
        select(TaskEvent).order_by(TaskEvent.timestamp.desc()).limit(limit)
    )
    return result.scalars().all()
