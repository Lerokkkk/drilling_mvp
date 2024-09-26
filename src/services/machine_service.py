from sqlalchemy.ext.asyncio import AsyncSession

from src.machines.crud import MachineCrud


class MachineService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.machine_crud = MachineCrud(db)

    async def create_machine(self, dto):
        return await self.machine_crud.create(dto)

    async def read_machine(self, obj_id):
        return await self.machine_crud.read(obj_id)

    async def update_machine(self, obj_id, dto):
        return await self.machine_crud.update(obj_id, dto)

    async def delete_machine(self, obj_id):
        return await self.machine_crud.delete(obj_id)
