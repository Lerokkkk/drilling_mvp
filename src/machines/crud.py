from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Machine
from src.utils import BaseCrud


class MachineCrud(BaseCrud):
    def __init__(self, db: AsyncSession):
        super().__init__(model=Machine, db=db)


async def get_machines(db: AsyncSession):
    res = await db.execute(select(Machine))
    return res.scalars().all()
