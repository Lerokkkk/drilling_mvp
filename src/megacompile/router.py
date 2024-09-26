from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_db
from src.megacompile.crud import MegaCompileCrud
from src.megacompile.schemas import BaseMegaCompile

mega_compile_router = APIRouter(prefix='/megacompile', tags=['megacompile'])


@mega_compile_router.get('/{mega_compile_id}')
async def get_mega_compile(mega_compile_id: int, db: AsyncSession = Depends(get_db)):
    return await MegaCompileCrud(db).read(mega_compile_id)


@mega_compile_router.post('/{mega_compile_id}')
async def create_mega_compile(dto: list[BaseMegaCompile], db: AsyncSession = Depends(get_db)):
    res = await MegaCompileCrud(db).create(dto)
    print(res)
    return "success"
