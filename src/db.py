from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from src.config import *

Base = declarative_base()

engine = create_async_engine(
    f"postgresql+asyncpg://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}:5432/{TEST_DB_NAME}",
    # f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
)

async_session = async_sessionmaker(engine, class_=AsyncSession)


async def get_db() -> AsyncGenerator:
    async with async_session() as session:
        yield session
