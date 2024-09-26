from src.machines.crud import MachineCrud
from src.names.crud import NameCrud
from src.utils import RelationObjectsMixin


class MachineNamesService(RelationObjectsMixin):
    def __init__(self, db):
        self.db = db
        self.machine_crud = MachineCrud(db)

    async def add_names_to_machine(self, machine_id: int, names_ids: list[int]):
        machine = await self.machine_crud.read(machine_id, related_field='names')

        names = await NameCrud(self.db).get_names_by_id(names_ids)

        res = await self.add_related_objects(machine, names, relation_field='names')

        return res

    async def delete_names(self, machine_id: int):
        machine = await self.machine_crud.read(machine_id, related_field='names')
        return await self.delete_related_objects(machine, 'names')

    async def update_names_to_machine(self, machine_id: int, names_ids: list[int]):
        machine = await self.machine_crud.read(machine_id, related_field='names')

        names = await NameCrud(self.db).get_names_by_id(names_ids)

        res = await self.update_related_field(machine, names, relation_field='names')
        return res

    async def read_machine_with_names(self, machine_id: int):
        return await self.machine_crud.read(machine_id, related_field='names')