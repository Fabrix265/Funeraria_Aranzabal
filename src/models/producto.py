from sqlmodel import SQLModel, Field

class Producto(SQLModel, table=True):
    id: int = Field(primary_key=True)
    nombre: str = Field()
    descripcion: str = Field()
    cantidad: int = Field()
    precio: float = Field()