from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.db import get_db
from src.machines.schemas import ShowMachine, CreateMachine, UpdateMachine
from .crud import MachineCrud
from ..models import Name, Machine
from ..names.crud import NameCrud

machine_router = APIRouter(prefix='/machine', tags=['machine'])


@machine_router.post("/", response_model=ShowMachine)
async def create_machine_view(machine: CreateMachine, db: AsyncSession = Depends(get_db)):
    machine_db = MachineCrud(db)
    res = await machine_db.create(machine)
    return res


@machine_router.get("/machines", response_model=list[ShowMachine])
async def read_machines_view(db: AsyncSession = Depends(get_db)):
    machine_crud = MachineCrud(db)
    res = await machine_crud.get_machines()
    print(res)
    return res


@machine_router.get("/{machine_id}", response_model=ShowMachine)
async def read_machine_view(machine_id: int, db: AsyncSession = Depends(get_db)):
    res = MachineCrud(db)
    return await res.read(machine_id)


@machine_router.patch("/{machine_id}", response_model=ShowMachine)
async def update_machine_view(machine_id: int, dto: UpdateMachine, db: AsyncSession = Depends(get_db)):
    machine_db = MachineCrud(db)
    res = await machine_db.update(machine_id, dto)
    return res


@machine_router.delete("/{machine_id}")
async def delete_machine_view(machine_id: int, db: AsyncSession = Depends(get_db)):
    machine_db = MachineCrud(db)
    return await machine_db.delete(machine_id)


@machine_router.post("/{machine_id}/names")
async def add_machines(machine_id: int, names_ids: list[int], db: AsyncSession = Depends(get_db)):
    crud = MachineCrud(db)
    options = [selectinload(Machine.names)]
    names = await NameCrud(db).get_names_by_id(names_ids)
    await crud.add_names_to_machine(machine_id, names, options=options)
    return {"name_id": machine_id,
            "machines_ids": names_ids}
