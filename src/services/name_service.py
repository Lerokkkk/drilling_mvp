from sqlalchemy.ext.asyncio import AsyncSession

from src.names.crud import NameCrud


class NameService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.name_crud = NameCrud(db)

    async def create_name(self, dto):

        if isinstance(dto, list):
            dto_list = list()
            for i in dto:
                dto_list.append(i.model_dump())
            return await self.name_crud.bulk_create(dto_list)

        return await self.name_crud.create(dto)

    async def read_name(self, obj_id):
        return await self.name_crud.read(obj_id)

    async def update_name(self, obj_id, dto):
        return await self.name_crud.update(obj_id, dto)

    async def delete_name(self, obj_id):
        return await self.name_crud.delete(obj_id)
