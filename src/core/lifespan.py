from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel
from src.config.db import engine

from src.models import User, Servicio, Ataud, Capilla, Vehiculo, Contratante, Fallecido, ServicioVehiculo

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    print("tablas creadas")
    print("Tablas registradas:", SQLModel.metadata.tables.keys())
    yield
