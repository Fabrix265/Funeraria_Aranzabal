from typing import List, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

class Venta(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fecha: datetime = Field(default_factory=datetime.utcnow)

    productos: List["VentaProducto"] = Relationship(back_populates="venta")
