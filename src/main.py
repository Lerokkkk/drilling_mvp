import uvicorn
from fastapi import FastAPI
from src.machine_names.router import machine_name_router
from src.machines.router import machine_router
from src.megacompile.router import mega_compile_router
from src.names.router import name_router
from src.names_machines.router import name_machine_router

app = FastAPI()

app.include_router(
    machine_router
)

app.include_router(
    name_router
)

app.include_router(
    name_machine_router
)

app.include_router(
    machine_name_router
)

app.include_router(
    mega_compile_router
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, env_file='.env.dev')
