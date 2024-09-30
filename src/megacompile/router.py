import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_db
from src.megacompile.crud import MegaCompileCrud
from src.megacompile.schemas import CreateMegaCompiles, ShowDateTimes, ValueTimeMegaCompile, MachineNameMegaCompile
from src.services.megacompiles_service import MegaCompileService

mega_compile_router = APIRouter(prefix='/megacompile', tags=['megacompile'])


@mega_compile_router.get('/{mega_compile_id}')
async def get_mega_compile(mega_compile_id: int, db: AsyncSession = Depends(get_db)):
    return await MegaCompileCrud(db).read(mega_compile_id)


@mega_compile_router.post('/machine/{machine_id}/name/{name_id}', response_model=list[ShowDateTimes])
async def create_mega_compile(machine_id: int, name_id: int, dto: list[CreateMegaCompiles],
                              db: AsyncSession = Depends(get_db)):
    res = await MegaCompileService(db).create_mega_compile(machine_id, name_id, dto)
    return [ShowDateTimes(get_time=item) for item in res]


@mega_compile_router.get('/1213/machine/{machine_id}/name/{name_id}', response_model=list[ValueTimeMegaCompile])
async def get_mega_compiles(machine_id: int, name_id: int, db: AsyncSession = Depends(get_db)):
    res = await MegaCompileService(db).get_mega_compile_by_fk(machine_id, name_id)
    print(res)
    temp = res[0]
    print(MachineNameMegaCompile(compile_data=temp[0], machine_name=temp[1], name=temp[2]))
    return res


@mega_compile_router.get('hello')
async def hello():
    return "hello"
