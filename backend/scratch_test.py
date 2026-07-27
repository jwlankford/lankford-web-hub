import asyncio
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
# Clean/Format URL like in config.py
url = DATABASE_URL
if url.startswith("postgresql://"):
    url = url.replace("postgresql://", "postgresql+asyncpg://")
if "?" in url:
    url, _ = url.split("?")

print("Cleaned ASYNC_DATABASE_URL:", url)

async def test_sqlalchemy():
    # Test with ssl=True
    print("\nTesting SQLAlchemy with ssl=True...")
    engine = create_async_engine(
        url,
        connect_args={"ssl": True}
    )
    try:
        async with engine.connect() as conn:
            print("SUCCESS with ssl=True in SQLAlchemy!")
        await engine.dispose()
    except Exception as e:
        print(f"FAILED with ssl=True: {e}")

    # Test with ssl='require'
    print("\nTesting SQLAlchemy with ssl='require'...")
    engine_require = create_async_engine(
        url,
        connect_args={"ssl": "require"}
    )
    try:
        async with engine_require.connect() as conn:
            print("SUCCESS with ssl='require' in SQLAlchemy!")
        await engine_require.dispose()
    except Exception as e:
        print(f"FAILED with ssl='require': {e}")

asyncio.run(test_sqlalchemy())
