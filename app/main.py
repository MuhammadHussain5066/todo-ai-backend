from app.routers.ai import router as ai_router
from fastapi import FastAPI
from sqlmodel import SQLModel
from app.db import engine
from app.routers.task import router as task_router

app = FastAPI(
    title="Todo AI Chatbot — Phase III",
    version="0.1.0"
)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

@app.get("/")
async def root():
    return {"status": "ok", "message": "Todo AI backend running"}

app.include_router(task_router)
app.include_router(ai_router)



