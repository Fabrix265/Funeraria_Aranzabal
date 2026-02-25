from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class Producto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)    
    nombre: str = Field()
    descripcion: str = Field()
    stock: int = Field()
    precio: float = Field()
