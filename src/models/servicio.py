from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import date
from enum import Enum

from src.models.fallecido import Fallecido

class TipoPago(str, Enum):
    directo = "directo"
    seguro = "seguro"

class Servicio(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # FKs
    id_usuario: int = Field(foreign_key="user.id", nullable=False)
    id_ataud: Optional[int] = Field(default=None, foreign_key="ataud.id")
    id_capilla: int = Field(foreign_key="capilla.id", nullable=False)
    id_contratante: int = Field(foreign_key="contratante.id", nullable=False)
    id_fallecido: int = Field(foreign_key="fallecido.id", nullable=False, unique=True)
    # Datos
    direccion_velacion: str = Field(nullable=False, max_length=200)
    tipo_pago: TipoPago = Field(nullable=False, index=True)
    arreglo_flora: bool = Field(default=False)
    fecha: date = Field(nullable=False, index=True)
    
    # Logística
    cantidad_cargadores: Optional[int] = Field(default=None)
    director_sepelio: bool = Field(default=False)

    # Relaciones
    usuario: "User" = Relationship(back_populates="servicios")
    ataud: Optional["Ataud"] = Relationship(back_populates="servicios")
    capilla: "Capilla" = Relationship(back_populates="servicios")
    contratante: "Contratante" = Relationship(back_populates="servicios")

    fallecido: "Fallecido" = Relationship(back_populates="servicio")

    vehiculos_asignados: List["ServicioVehiculo"] = Relationship(back_populates="servicio")