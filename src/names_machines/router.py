from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.db import get_db
from src.machines.crud import MachineCrud
from src.models import Name
from src.names.crud import NameCrud

name_machine_router = APIRouter(prefix='/name', tags=["name-machines"])


@name_machine_router.post("/{name_id}/machines")
async def add_machines(name_id: int, machines_ids: list[int], db: AsyncSession = Depends(get_db)):
    crud = NameCrud(db)
    res = await crud.add_machines_to_name(name_id, machines_ids)
    return {"name_id": name_id,
            "machines_ids": machines_ids}


@name_machine_router.delete("/{name_id}/machines")
async def delete_machines(name_id: int, db: AsyncSession = Depends(get_db)):
    name_crud = await NameCrud(db).delete_machines(name_id)
    return name_crud
