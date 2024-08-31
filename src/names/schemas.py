from pydantic import BaseModel


class BaseName(BaseModel):
    name: str


class ShowName(BaseName):
    id: int


class CreateName(BaseName):
    pass


class ExName(BaseName):
    imp: int = 10
