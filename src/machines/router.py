from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_db
from src.machines.schemas import ShowMachine, CreateMachine, UpdateMachine
from .crud import MachineCrud, get_machines

machine_router = APIRouter(prefix='/machine', tags=['machine'])


@machine_router.post("/", response_model=ShowMachine)
async def create_machine_view(machine: CreateMachine, db: AsyncSession = Depends(get_db)):
    machine_db = MachineCrud(db)
    res = await machine_db.create(machine)
    return res


@machine_router.get("/machines", response_model=list[ShowMachine])
async def read_machines_view(db: AsyncSession = Depends(get_db)):
    res = await get_machines(db)
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
