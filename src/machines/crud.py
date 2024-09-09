from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models import Machine, Name
from src.utils import BaseCrudMixin


class MachineCrud(BaseCrudMixin):
    def __init__(self, db: AsyncSession):
        super().__init__(model=Machine, db=db)

    async def get_machines_by_ids(self, ids: list[int]):
        machines = await self.db.execute(select(self.model).filter(self.model.id.in_(ids)))
        machines = machines.scalars().all()
        return machines

    async def get_machines(self):
        res = await self.db.execute(select(self.model))
        return res.scalars().all()

    async def add_names_to_machine(self, machine_id: int, names: list[Name], options: list[selectinload] = None):
        machine = await self.read(machine_id, options)
        print(getattr(machine, "names"))

        machine.names.update(names)
        try:
            await self.db.commit()

        except Exception as e:
            print(e)
        return names
