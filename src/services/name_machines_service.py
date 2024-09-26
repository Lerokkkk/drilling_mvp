from sqlalchemy.ext.asyncio import AsyncSession

from ..machines.crud import MachineCrud
from ..names.crud import NameCrud
from ..utils import RelationObjectsMixin


class NameMachinesService(RelationObjectsMixin):

    def __init__(self, db: AsyncSession):
        self.db = db
        self.name_crud = NameCrud(db)

    async def add_machines_to_name(self, name_id: int, machines_ids: list[int]):
        name = await self.name_crud.read(name_id, related_field='machines')

        machines = await MachineCrud(self.db).get_machines_by_ids(machines_ids)

        res = await self.add_related_objects(name, machines, relation_field='machines')
        return res

    async def delete_machines(self, name_id: int):
        name = await self.name_crud.read(name_id, related_field='machines')
        return await self.delete_related_objects(name, 'machines')

    async def update_machines_to_name(self, name_id: int, machines_ids: list[int]):
        name = await self.name_crud.read(name_id, related_field='machines')

        machines = await MachineCrud(self.db).get_machines_by_ids(machines_ids)
        print(f'имя: {name}, машины: {machines}')

        res = await self.update_related_field(name, machines, relation_field='machines')
        return res

    async def read_name_with_machines(self, name_id: int):
        return await self.name_crud.read(name_id, related_field='machines')
