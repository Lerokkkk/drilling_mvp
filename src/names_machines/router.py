from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from ..machines.schemas import ShowMachine
from .schemas import ShowNamesMachine
from src.db import get_db
from src.services.name_machines_service import NameMachinesService

name_machine_router = APIRouter(prefix='/name', tags=["name-machines"])


@name_machine_router.post("/{name_id}/machines")
async def add_machines(name_id: int, machines_ids: list[int], db: AsyncSession = Depends(get_db)):
    res = await NameMachinesService(db).add_machines_to_name(name_id, machines_ids)
    return {"name_id": name_id,
            "machines_ids": machines_ids}


@name_machine_router.delete("/{name_id}/machines")
async def delete_machines(name_id: int, db: AsyncSession = Depends(get_db)):
    name_crud = await NameMachinesService(db).delete_machines(name_id)
    return name_crud


@name_machine_router.put("/{name_id}/machines", response_model=list[ShowMachine])
async def update_machines(name_id: int, machines_ids: list[int], db: AsyncSession = Depends(get_db)):
    res = await NameMachinesService(db).update_machines_to_name(name_id, machines_ids)
    return res


@name_machine_router.get("/{name_id}/machines", response_model=ShowNamesMachine)
async def get_machines(name_id: int, db: AsyncSession = Depends(get_db)):
    res = await NameMachinesService(db).read_name_with_machines(name_id)
    print(res.machines)
    return res
