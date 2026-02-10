from fastapi import APIRouter
from src.deps.db_session import SessionDep
from src.schemas.producto import ProductoCrear, ProductoModificar, ProductoLeer
from src.services.producto_service import crear_producto
from src.services.producto_service import (
    obtener_productos,
    crear_producto,
    actualizar_producto,
    eliminar_producto
)

producto_router = APIRouter()

@producto_router.get("/", response_model=list[ProductoLeer], tags=["Inventario"])
def obtener_productos_endpoint(db: SessionDep):
    return obtener_productos(db)

@producto_router.post("/", response_model=ProductoLeer, tags=["Inventario"])
def crear_producto_endpoint(producto: ProductoCrear, db: SessionDep):
    return crear_producto(db, producto)

@producto_router.put("/{id}", response_model=ProductoLeer, tags=["Inventario"])
def actualizar_producto_endpoint(id: int, producto: ProductoModificar, db: SessionDep):
    return actualizar_producto(db, id, producto)
    
@producto_router.delete("/{id}", tags=["Inventario"])
def eliminar_producto_endpoint(id: int, db: SessionDep):
    eliminar_producto(db, id)
    return {"message": "Producto eliminado correctamente"}
