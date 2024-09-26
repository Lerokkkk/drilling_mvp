from pydantic import BaseModel


class BaseName(BaseModel):
    name: str

    class Config:
        from_attributes = True


class ShowName(BaseName):
    id: int


class CreateName(BaseName):
    pass
