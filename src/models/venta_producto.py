from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class VentaProducto(SQLModel, table=True):
    venta_id: Optional[int] = Field(
        default=None,
        foreign_key="venta.id",
        primary_key=True
    )
    producto_id: Optional[int] = Field(
        default=None,
        foreign_key="producto.id",
        primary_key=True
    )

    cantidad: int
    precio_unitario: float

    venta: Optional["Venta"] = Relationship(back_populates="productos")
    producto: Optional["Producto"] = Relationship(back_populates="ventas")
