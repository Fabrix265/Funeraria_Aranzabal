from pydantic import BaseModel
from src.models.vehiculo import TipoVehiculo

class VehiculoBase(BaseModel):
    tipo: TipoVehiculo

class VehiculoCrear(VehiculoBase):
    pass

class VehiculoLeer(VehiculoBase):
    id: int