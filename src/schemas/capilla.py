from pydantic import BaseModel, Field

class CapillaBase(BaseModel):
    modelo: str = Field(min_length=1, max_length=100)

class CapillaCrear(CapillaBase):
    pass

class CapillaLeer(CapillaBase):
    id: int
