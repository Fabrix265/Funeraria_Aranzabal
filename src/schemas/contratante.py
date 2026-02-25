from pydantic import BaseModel, Field

class ContratanteBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    dni: str = Field(pattern=r"^\d{8}$")
    telefono: str = Field(pattern=r"^9\d{8}$")

class ContratanteCrear(ContratanteBase):
    pass

class ContratanteLeer(ContratanteBase):
    id: int