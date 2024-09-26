from abc import ABC, abstractmethod
from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import TypeVar, Generic

from sqlalchemy.orm import selectinload

from src.db import Base


class AbstractCrud(ABC):
    def __init__(self, model, db: AsyncSession):
        self.model = model
        self.db = db

    @abstractmethod
    async def create(self, dto):
        pass

    @abstractmethod
    async def read(self, obj_id: int):
        pass

    @abstractmethod
    async def update(self, obj_id: int, dto):
        pass

    @abstractmethod
    async def delete(self, obj_id: int):
        pass


class BaseCrudMixin(AbstractCrud):
    async def create(self, dto):
        db_obj = self.model(**dto.model_dump())
        self.db.add(db_obj)
        try:
            await self.db.commit()
        except IntegrityError:
            raise HTTPException(status_code=409, detail=f"Имя '{dto.name}' уже существует в базе данных.")

        await self.db.refresh(db_obj)
        return db_obj

    async def read(self, obj_id: int, related_field: str = None):
        if related_field:
            options = [selectinload(getattr(self.model, related_field))]
            db_obj = await self.db.get(self.model, obj_id, options=options)
        else:
            db_obj = await self.db.get(self.model, obj_id)
        if db_obj is None:
            raise HTTPException(status_code=404, detail=f'{self.model.__name__} not found')
        return db_obj

    async def update(self, obj_id, dto):
        db_obj = await self.read(obj_id)
        q = update(self.model).filter(self.model.id == obj_id).values(dto.model_dump(exclude_unset=True))
        await self.db.execute(q)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def delete(self, obj_id: int):
        db_obj = await self.read(obj_id)
        await self.db.delete(db_obj)
        await self.db.commit()
        return {"result": "success"}


ModelType = TypeVar("ModelType", bound=Base)


class RelationObjectsMixin(Generic[ModelType]):
    async def add_related_objects(self, obj: ModelType, related_objects: list[ModelType], relation_field: str):
        update_field = getattr(obj, relation_field)
        update_field.update(related_objects)
        await self.db.commit()
        return related_objects

    async def delete_related_objects(self, obj: ModelType, relation_field: str):
        update_field = getattr(obj, relation_field)
        update_field.clear()
        await self.db.commit()
        return {"result": "success"}

    async def update_related_field(self, obj: ModelType, related_objects: list[ModelType], relation_field: str):
        update_field = getattr(obj, relation_field)
        update_field.clear()
        update_field.update(related_objects)
        print(related_objects)
        await self.db.commit()
        await self.db.refresh(obj)

        res = getattr(obj, relation_field)
        return res

