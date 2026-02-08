from fastapi import APIRouter, Depends
from sqlmodel import select
from app.db import get_session
from app.models.task import Task
from sqlalchemy.ext.asyncio import AsyncSession

# Groq / LLM
from openai import OpenAI
import os

router = APIRouter(prefix="/api/chat", tags=["Chat"])

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

@router.post("/")
async def chat(message: str, session: AsyncSession = Depends(get_session)):
    """
    Simple AI chat → task intent
    """

    prompt = f"""
You are a Todo assistant.

User message: "{message}"

If user wants to create a task, respond as:
CREATE: <task title>

If user wants to list tasks:
LIST

Otherwise:
CHAT: <normal reply>
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    reply = response.choices[0].message.content.strip()

    # 🟡 CREATE TASK
    if reply.startswith("CREATE:"):
        title = reply.replace("CREATE:", "").strip()
        task = Task(title=title)
        session.add(task)
        await session.commit()
        return {"action": "created", "task": title}

    # 🟢 LIST TASKS
    if reply.startswith("LIST"):
        result = await session.execute(select(Task))
        tasks = result.scalars().all()
        return {"action": "list", "tasks": tasks}

    # 🔵 NORMAL CHAT
    return {"action": "chat", "reply": reply}
