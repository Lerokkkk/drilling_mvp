from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_db
from src.models import Name
from src.services.name_service import NameService
from src.names.schemas import BaseName, CreateName, ShowName

name_router = APIRouter(prefix='/name', tags=["name"])


@name_router.get("/all", response_model=list[ShowName])
async def read_names_view(limit: int = 1000, db: AsyncSession = Depends(get_db)):
    stmt = select(Name).limit(limit)
    print(stmt.compile(dialect=db.bind.dialect, compile_kwargs={'literal_binds': True}))
    res = await db.execute(stmt)
    names = res.scalars().all()
    print(names[0].name)
    return names


@name_router.get("/{name_id}", response_model=BaseName)
async def read_name_view(name_id: int, db: AsyncSession = Depends(get_db)):
    return await NameService(db).read_name(name_id)


@name_router.delete("/{name_id}")
async def delete_name_view(name_id: int, db: AsyncSession = Depends(get_db)):
    return await NameService(db).delete_name(name_id)


@name_router.post("/", response_model=list[ShowName] | ShowName)
async def create_name_view(name: CreateName | list[CreateName], db: AsyncSession = Depends(get_db)):
    return await NameService(db).create_name(name)


@name_router.patch("/{name_id}", response_model=ShowName)
async def update_name_view(name_id: int, dto: BaseName, db: AsyncSession = Depends(get_db)):
    return await NameService(db).update_name(name_id, dto)
