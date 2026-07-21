from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from config import settings

# 1. Create the asynchronous database engine
engine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    echo=True, # Set to False in production to reduce log noise
    future=True
)

# 2. Create a session factory to generate isolated request sessions
async_session_maker = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# 3. Dynamic initialization function executed on app startup
async def init_db() -> None:
    # Ensure all your SQLModel tables are discovered and imported before calling this
    import models  
    
    async with engine.begin() as conn:
        # Automatically generate missing tables safely
        await conn.run_sync(SQLModel.metadata.create_all)

# 4. Dependency injection helper for FastAPI routes
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session