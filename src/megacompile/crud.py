from fastapi import HTTPException
from sqlalchemy import select, and_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only

from src.models import MegaCompile, Machine, Name
from src.utils import BaseCrudMixin


class MegaCompileCrud(BaseCrudMixin):
    def __init__(self, db: AsyncSession):
        super().__init__(model=MegaCompile, db=db)

    async def create(self, dto: list):
        stmt = insert(self.model).returning(self.model.get_time)
        print(dto)
        print(stmt.compile(dialect=self.db.bind.dialect, compile_kwargs={'literal_binds': True}))

        try:
            res_stmt = await self.db.execute(stmt, dto)
            await self.db.flush()

            inserted_rows = res_stmt.scalars().fetchall()

            await self.db.commit()
        except IntegrityError as e:
            raise HTTPException(status_code=404, detail=f'{e.orig}')

        return inserted_rows

    async def read_by_fk(self, machine_id: int, name_id: int):
        query = (select(self.model, Machine.machine_name, Name.name)
                 .join(Machine)
                 .join(Name)
                 .where(and_(
                    self.model.machine_id == machine_id,
                    self.model.name_id == name_id)
        ).options(load_only(self.model.value, self.model.get_time)))
        print(query.compile(dialect=self.db.bind.dialect, compile_kwargs={'literal_binds': True}))
        res = await self.db.execute(query)
        return res.fetchall()
