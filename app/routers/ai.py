from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from app.models.task import Task
from datetime import datetime

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/task")
async def create_task_from_text(
    text: str,
    session: AsyncSession = Depends(get_session)
):
    """Simple task creation"""
    try:
        # Simple task - no AI
        new_task = Task(
            title=text[:100],
            description="Created via AI",
            completed=False,
            due_date=None
        )
        
        session.add(new_task)
        await session.commit()
        await session.refresh(new_task)
        
        return {"id": new_task.id, "title": new_task.title}
        
    except Exception as e:
        print(f"ERROR: {e}")
        await session.rollback()
        return {"error": str(e)}
