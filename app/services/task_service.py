from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import Task


async def create_task(session: AsyncSession, task: Task) -> Task:
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def get_tasks(session: AsyncSession):
    result = await session.execute(select(Task))
    return result.scalars().all()


async def get_task_by_id(session: AsyncSession, task_id: int):
    return await session.get(Task, task_id)


async def update_task(session: AsyncSession, task_id: int, data: dict):
    task = await session.get(Task, task_id)
    if not task:
        return None

    for key, value in data.items():
        setattr(task, key, value)

    await session.commit()
    await session.refresh(task)
    return task


async def delete_task(session: AsyncSession, task_id: int):
    task = await session.get(Task, task_id)
    if not task:
        return False

    await session.delete(task)
    await session.commit()
    return True
