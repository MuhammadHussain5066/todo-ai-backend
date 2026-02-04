from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.models.task import Task
from app.services.task_service import (
    create_task,
    get_tasks,
    get_task_by_id,
    update_task,
    delete_task
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=Task)
async def create(task: Task, session: AsyncSession = Depends(get_session)):
    return await create_task(session, task)


@router.get("/", response_model=list[Task])
async def list_tasks(session: AsyncSession = Depends(get_session)):
    return await get_tasks(session)


@router.get("/{task_id}", response_model=Task)
async def get(task_id: int, session: AsyncSession = Depends(get_session)):
    task = await get_task_by_id(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=Task)
async def update(task_id: int, data: dict, session: AsyncSession = Depends(get_session)):
    task = await update_task(session, task_id, data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}")
async def delete(task_id: int, session: AsyncSession = Depends(get_session)):
    success = await delete_task(session, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"ok": True}
