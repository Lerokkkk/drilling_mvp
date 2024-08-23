from fastapi import FastAPI, HTTPException
from src.machines.router import machine_router

app = FastAPI()

app.include_router(
    machine_router
)

