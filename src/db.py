from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from src.settings.config import *

Base = declarative_base()

engine = create_async_engine(
    f"postgresql+asyncpg://{settings.db_user}:{settings.db_password}@{settings.db_host}:5432/{settings.db_name}"
)

async_session = async_sessionmaker(engine, class_=AsyncSession)


async def get_db() -> AsyncGenerator:
    async with async_session() as session:
        yield session
