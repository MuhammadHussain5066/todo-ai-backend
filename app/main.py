from app.routers.events import router as events_router
from app.models.event import TaskEvent
from app.routers.chat.router import router as chat_router
from app.routers.ai import router as ai_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from app.db import engine
from app.routers.task import router as task_router

app = FastAPI(
    title="Todo AI Chatbot — Phase III",
    version="0.1.0"
)

# CORS middleware - Allow production frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "https://todo-ai-frontend-one.vercel.app",
        "*"  # Temporary - allow all for testing
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

@app.get("/")
async def root():
    return {"status": "ok", "message": "Todo AI backend running"}

app.include_router(chat_router)
app.include_router(task_router)
app.include_router(ai_router)
app.include_router(events_router)
