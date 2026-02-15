from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from app.services.event_service import get_task_history, get_recent_events

router = APIRouter(prefix="/events", tags=["Events"])

@router.get("/task/{task_id}")
async def get_task_events(
    task_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Get event history for a specific task"""
    events = await get_task_history(session, task_id)
    return {
        "task_id": task_id,
        "events": [
            {
                "id": e.id,
                "event_type": e.event_type,
                "user_id": e.user_id,
                "timestamp": e.timestamp,
                "old_data": e.old_data,
                "new_data": e.new_data
            }
            for e in events
        ]
    }

@router.get("/recent")
async def get_recent_activity(
    limit: int = 50,
    session: AsyncSession = Depends(get_session)
):
    """Get recent events across all tasks"""
    events = await get_recent_events(session, limit)
    return {
        "events": [
            {
                "id": e.id,
                "task_id": e.task_id,
                "event_type": e.event_type,
                "user_id": e.user_id,
                "timestamp": e.timestamp
            }
            for e in events
        ]
    }
