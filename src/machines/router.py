from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_db
from src.machines.schemas import ShowMachine, CreateMachine, UpdateMachine
from ..services.machine_service import MachineService

machine_router = APIRouter(prefix='/machine', tags=['machine'])


@machine_router.post("/", response_model=ShowMachine)
async def create_machine_view(machine: CreateMachine, db: AsyncSession = Depends(get_db)):
    return await MachineService(db).create_machine(machine)


@machine_router.get("/{machine_id}", response_model=ShowMachine)
async def read_machine_view(machine_id: int, db: AsyncSession = Depends(get_db)):
    return await MachineService(db).read_machine(machine_id)


@machine_router.patch("/{machine_id}", response_model=ShowMachine)
async def update_machine_view(machine_id: int, dto: UpdateMachine, db: AsyncSession = Depends(get_db)):
    return await MachineService(db).update_machine(machine_id, dto)


@machine_router.delete("/{machine_id}")
async def delete_machine_view(machine_id: int, db: AsyncSession = Depends(get_db)):
    return await MachineService(db).delete_machine(machine_id)
