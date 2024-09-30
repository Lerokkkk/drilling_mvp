from datetime import datetime

from pydantic import BaseModel


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


class MachineNameMegaCompile(BaseModel):
    compile_data: ValueTimeMegaCompile
    machine_name: str
    name: str
