from fastapi import HTTPException

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Machine
from src.machines.schemas import CreateMachine, UpdateMachine


async def find_machine(machine_id: int, db):
    machine = await db.get(Machine, machine_id)
    return machine


async def create_machine(machine: CreateMachine, db):
    print(machine.model_dump())
    db_machine = Machine(**machine.model_dump())
    db.add(db_machine)
    await db.commit()
    await db.refresh(db_machine)
    return db_machine


async def get_machines(db: AsyncSession):
    res = await db.execute(select(Machine))
    return res.scalars().all()


async def update_machine(machine_id: int, dto: UpdateMachine, db: AsyncSession):
    db_machine = await find_machine(machine_id, db)
    if db_machine is None:
        raise HTTPException(status_code=404, detail='Machine not found')
    q = update(Machine).filter(Machine.id == machine_id).values(dto.model_dump(exclude_unset=True))
    await db.execute(q)
    await db.commit()
    await db.refresh(db_machine)
    return db_machine


async def delete_machine(machine_id: int, db: AsyncSession):
    db_machine = await find_machine(machine_id, db)
    if db_machine is None:
        raise HTTPException(status_code=404, detail='Machine not found')
    await db.delete(db_machine)
    await db.commit()
    return {"machine_id": machine_id}
