from datetime import datetime

from pydantic import BaseModel
from sqlalchemy.sql.coercions import cls
from typing_extensions import Any, Self


class BaseMegaCompile(BaseModel):
    value: float
    get_time: datetime
    analog: bool
    unit: str
    name_id: int
    machine_id: int

    class Config:
        from_attributes = True


class CreateMegaCompiles(BaseModel):
    value: float
    get_time: datetime
    analog: bool
    unit: str


class ShowDateTimes(BaseModel):
    get_time: datetime


class ValueTimeMegaCompile(BaseModel):
    value: float
    get_time: datetime

    @classmethod
    def from_orm(cls, obj: Any) -> Self:
        return cls(value=obj.value, get_time=obj.get_time)


class MachineNameMegaCompile(BaseModel):
    compile_data: ValueTimeMegaCompile
    machine_name: str
    name: str

    @classmethod
    def from_tuple(cls, obj_tuple):
        return cls(
            compile_data=ValueTimeMegaCompile.from_orm(obj_tuple[0]),
            machine_name=obj_tuple[1],
            name=obj_tuple[2]
        )

    class Config:
        from_attributes = True
