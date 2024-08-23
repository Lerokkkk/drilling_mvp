from fastapi import FastAPI, HTTPException
from src.machines.router import machine_router
from src.names.router import name_router

app = FastAPI()

app.include_router(
    machine_router
)


app.include_router(
    name_router
)

