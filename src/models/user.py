from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from enum import Enum

class CargoEnum(str, Enum):
    administrador = "administrador"
    trabajador = "trabajador"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(nullable=False, unique=True, index=True, max_length=30)
    password: str = Field(nullable=False)
    cargo: CargoEnum = Field(nullable=False, index=True)

    servicios: List["Servicio"] = Relationship(back_populates="usuario")