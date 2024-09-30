from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.machines.crud import MachineCrud
from src.megacompile.crud import MegaCompileCrud
from src.names.crud import NameCrud
from src.megacompile.schemas import BaseMegaCompile


class MegaCompileService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.mega_compile_crud = MegaCompileCrud(db)
        self.machine_crud = MachineCrud(db)
        self.name_crud = NameCrud(db)

    async def create_mega_compile(self, machine_id: int, name_id: int, dto_list: list):
        machine = await self.machine_crud.read(machine_id, 'names')
        name = await self.name_crud.read(name_id)

        if name not in machine.names:
            raise HTTPException(status_code=404, detail="Machine and name are not linked")

        mega_compiles = [BaseMegaCompile(**dto.model_dump(), machine_id=machine_id, name_id=name_id) for dto in
                         dto_list]

        print(mega_compiles)

        return await self.mega_compile_crud.create(mega_compiles)
