from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from .crud import find_machine, create_machine, update_machine, delete_machine, get_machines
from src.db import get_db
from src.machines.schemas import ShowMachine, CreateMachine, UpdateMachine

machine_router = APIRouter(prefix='/machine')


@machine_router.post("/", response_model=ShowMachine)
async def create_machine_view(machine: CreateMachine, db: AsyncSession = Depends(get_db)):
    res = await create_machine(machine, db)
    print(res)
    return res


@machine_router.get("/machines", response_model=list[ShowMachine])
async def read_machines_view(db: AsyncSession = Depends(get_db)):
    res = await get_machines(db)
    print(res)
    return res


@machine_router.get("/{machine_id}", response_model=ShowMachine)
async def read_machine_view(machine_id: int, db: AsyncSession = Depends(get_db)):
    res = await find_machine(machine_id, db)
    if res is None:
        raise HTTPException(status_code=404, detail='Machine not found')
    return res


@machine_router.patch("/{machine_id}", response_model=ShowMachine)
async def update_machine_view(machine_id: int, dto: UpdateMachine, db: AsyncSession = Depends(get_db)):
    res = await update_machine(machine_id, dto, db)
    return res


@machine_router.delete("/{machine_id}")
async def delete_machine_view(machine_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_machine(machine_id, db)
