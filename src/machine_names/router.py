from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_db
from src.services.machine_names_service import MachineNamesService

machine_name_router = APIRouter(prefix='/machine', tags=["machines-names"])


@machine_name_router.post("/{machine_id}/names")
async def add_names(machine_id: int, names_ids: list[int], db: AsyncSession = Depends(get_db)):
    res = await MachineNamesService(db).add_names_to_machine(machine_id, names_ids)
    return {"name_id": machine_id,
            "machines_ids": names_ids}


@machine_name_router.get("/{machine_id}/names")
async def get_names(machine_id: int, db: AsyncSession = Depends(get_db)):
    return await MachineNamesService(db).read_machine_with_names(machine_id)


@machine_name_router.put("/{machine_id}/names")
async def update_names(machine_id: int, names_ids: list[int], db: AsyncSession = Depends(get_db)):
    return await MachineNamesService(db).update_names_to_machine(machine_id, names_ids)


@machine_name_router.delete("/{machine_id}/names")
async def delete_names(machine_id: int, db: AsyncSession = Depends(get_db)):
    return await MachineNamesService(db).delete_names(machine_id)
