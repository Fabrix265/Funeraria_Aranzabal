from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class VentaProductoCrear(BaseModel):
    producto_id: int
    cantidad: int = Field(gt=0)

class VentaCrear(BaseModel):
    productos: List[VentaProductoCrear]

class VentaProductoLeer(BaseModel):
    producto_id: int
    cantidad: int
    precio_unitario: float

class VentaLeer(BaseModel):
    id: int
    fecha: datetime
    productos: List[VentaProductoLeer]