from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_db
from src.models import Name

name_router = APIRouter(prefix='/name')


class BaseName(BaseModel):
    name: str


@name_router.get("/all", response_model=list[BaseName])
async def read_names_view(limit: int = 1000, db: AsyncSession = Depends(get_db)):
    stmt = select(Name)
    print(stmt.compile(dialect=db.bind.dialect, compile_kwargs={'literal_binds': True}))
    res = await db.execute(stmt)
    names = res.scalars().all()
    return names
