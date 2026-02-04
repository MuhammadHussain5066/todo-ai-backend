from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.db import get_session
from app.models.task import Task
from app.services.ai_service import extract_task_from_text

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/task")
async def create_task_from_text(
    text: str,
    session: AsyncSession = Depends(get_session)
):
    """
    Converts natural language into a task using AI
    """
    ai_task = await extract_task_from_text(text)

    task = Task(
        title=ai_task["title"],
        description=ai_task.get("description", "")
    )

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return {
        "status": "created",
        "task": task
    }
