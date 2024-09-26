from sqlalchemy import select
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.names.crud import NameCrud
from src.models import Machine, Name
from src.utils import BaseCrudMixin


class MachineCrud(BaseCrudMixin):
    def __init__(self, db: AsyncSession):
        super().__init__(model=Machine, db=db)

    async def get_machines_by_ids(self, ids: list[int]):
        q = select(self.model).filter(self.model.id.in_(ids))
        machines = await self.db.execute(q)
        machines = machines.scalars().all()
        return machines

    async def get_machines(self):
        res = await self.db.execute(select(self.model))
        return res.scalars().all()


