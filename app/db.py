import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# 1️⃣ Load environment variables
load_dotenv()  # Make sure your .env is in the project root

# 2️⃣ Get DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in environment variables")

# 3️⃣ Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    future=True,
)

# 4️⃣ Create async session factory
async_session = sessionmaker(
    engine,               # pass engine directly
    class_=AsyncSession,  # use AsyncSession class
    expire_on_commit=False
)

# 5️⃣ FastAPI dependency
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
