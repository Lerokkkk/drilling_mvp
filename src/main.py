import uvicorn
from fastapi import FastAPI, HTTPException
from src.machines.router import machine_router
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

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
