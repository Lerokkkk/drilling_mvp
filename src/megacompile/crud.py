from fastapi import HTTPException
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import MegaCompile
from src.utils import BaseCrudMixin


class MegaCompileCrud(BaseCrudMixin):
    def __init__(self, db: AsyncSession):
        super().__init__(model=MegaCompile, db=db)

    async def create(self, dto: list):
        stmt = insert(self.model).returning(self.model.get_time)
        print(stmt.compile(dialect=self.db.bind.dialect, compile_kwargs={'literal_binds': True}))

        try:
            res_stmt = await self.db.execute(stmt, dto)
            await self.db.flush()

            inserted_rows = res_stmt.scalars().fetchall()

            await self.db.commit()
        except IntegrityError as e:
            print(f'Ошибка: {e.__dict__}')
            raise HTTPException(status_code=404, detail=f'{e.orig}')

        return inserted_rows
