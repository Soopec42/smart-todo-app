from sqlalchemy.ext.asyncio import *
from sqlalchemy.orm import *
import os
from dotenv import load_dotenv

load_dotenv()
Database_URL = "postgresql+asyncpg://postgres:gumanoid99@localhost:5432/smart_todo"

engine = create_async_engine(Database_URL, echo = True)

AsyncSessionLocal = sessionmaker(
    bind = engine, 
    class_ = AsyncSession,
    expire_on_commit=False
    )

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()



