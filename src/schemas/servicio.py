from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import date
from src.models.servicio import TipoPago
class ServicioBase(BaseModel):
    id_usuario: int
    id_ataud: Optional[int] = None
    id_capilla: int
    id_contratante: int
    id_fallecido: int
    direccion_velacion: str
    tipo_pago: TipoPago
    arreglo_flora: bool = False
    fecha: date
    cantidad_cargadores: Optional[int] = None
    director_sepelio: bool = False

    @field_validator('cantidad_cargadores')
    @classmethod
    def validar_cargadores(cls, v):
        if v is not None and v not in [4, 6]:
            raise ValueError('La cantidad de cargadores debe ser 4, 6 o null')
        return v

class ServicioCrear(ServicioBase):
    ids_vehiculos: List[int] = []

class ServicioLeer(ServicioBase):
    id: int