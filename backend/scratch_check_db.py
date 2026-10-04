import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import os

DATABASE_URL = 'postgresql+asyncpg://neondb_owner:npg_ftjon8bCUkG9@ep-muddy-butterfly-ax4izts7-pooler.c-4.us-east-2.aws.neon.tech/neondb'

async def main():
    engine = create_async_engine(
        DATABASE_URL,
        connect_args={'ssl': 'require', 'statement_cache_size': 0}
    )
    try:
        async with engine.begin() as conn:
            # Check if column exists
            result = await conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='research_papers' and column_name='used_for';
            """))
            if result.fetchone():
                print('Column already exists')
            else:
                print('Column does not exist. Adding it...')
                await conn.execute(text('ALTER TABLE research_papers ADD COLUMN used_for VARCHAR;'))
                print('Column added successfully')
    except Exception as e:
        print('Error:', e)
    finally:
        await engine.dispose()

asyncio.run(main())
