from pydantic import BaseModel, Field
from typing import Optional


#Esquema para consultar y registrar datos
class ProductoBase(BaseModel):
    nombre: str = Field(min_length=1)
    descripcion: str = Field(min_length=1, max_length=100, default="Sin descripcion")
    cantidad: int = Field(gt=0, default=0)
    precio: float = Field(gt=0)
    
class ProductoCrear(ProductoBase):
    pass

class ProductoModificar(BaseModel):
    nombre: Optional[str] = Field(min_length=1)
    descripcion: Optional[str] = Field(min_length=1, max_length=100)
    cantidad: Optional[int] = Field(gt=0)
    precio: Optional[float] = Field(gt=0)

class ProductoLeer(ProductoBase):
    id: int


    """
    #Parece no usado porque salta primero la validacion de Field antes que la validacion personalizada
    @field_validator('nombre')
    @classmethod
    def validar_nombre(cls, v):
        if len(v) < 5 or len(v) > 10:
            raise ValueError('El nombre debe tener entre 5 y 10 caracteres')
        return v
    """

""""
gt: greater than
lt: less than
ge: greater equal
le: less equal
"""