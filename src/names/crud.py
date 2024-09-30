from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Name
from src.utils import BaseCrudMixin


class NameCrud(BaseCrudMixin):

    def __init__(self, db: AsyncSession):
        super().__init__(model=Name, db=db)

    async def bulk_create(self, l: list[dict]):
        stmt = insert(self.model).on_conflict_do_nothing(index_elements=['name']).returning(self.model.id,
                                                                                            self.model.name)
        print(stmt.compile(dialect=self.db.bind.dialect, compile_kwargs={'literal_binds': True}))
        res_stmt = await self.db.execute(stmt, l)

        names = res_stmt.fetchall()
        await self.db.commit()

        return names

    async def get_names_by_id(self, ids: list[int]):
        names = await self.db.execute(select(self.model).filter(self.model.id.in_(ids)))
        names = names.scalars().all()
        return names


