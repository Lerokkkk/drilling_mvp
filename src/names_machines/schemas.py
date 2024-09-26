from pydantic import BaseModel
from ..machines.schemas import ShowMachine


class ShowNamesMachine(BaseModel):
    id: int
    name: str
    machines: list[ShowMachine]
