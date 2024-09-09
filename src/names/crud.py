from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.machines.crud import MachineCrud
from src.models import Name, Machine
from src.utils import BaseCrudMixin, RelationObjectsMixin


class NameCrud(BaseCrudMixin, RelationObjectsMixin):
    # related_field = Machine

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

    async def add_machines_to_name(self, name_id: int, machines_ids: list[int]):
        name = await self.read(name_id, related_field='machines')
        print(name.__dict__)

        machines = await MachineCrud(self.db).get_machines_by_ids(machines_ids)

        res = await self.add_related_objects(name, machines, relation_field='machines')
        # print(res)
        return res

    async def delete_machines(self, name_id: int):
        name = await self.read(name_id, related_field='machines')
        return await self.delete_related_objects(name, 'machines')
