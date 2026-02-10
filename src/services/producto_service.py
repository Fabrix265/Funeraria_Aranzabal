from fastapi import HTTPException
from src.models import Producto
from src.deps.db_session import SessionDep
from src.schemas.producto import ProductoCrear, ProductoModificar, ProductoLeer
from sqlmodel import select
from starlette import status


def obtener_productos(db: SessionDep) -> list[Producto]:
    statement = select(Producto)
    result = db.exec(statement).all()
    return result

def crear_producto(db: SessionDep, producto: ProductoCrear) -> Producto:
    db_producto = Producto(**producto.model_dump())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

def actualizar_producto(db: SessionDep, id: int, producto: ProductoModificar) -> Producto:
    producto_db = db.get(Producto, id)
    if not producto_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    data = producto.model_dump(exclude_unset=True)
    for campo, valor in data.items():
        setattr(producto_db, campo, valor)
    db.commit()
    db.refresh(producto_db)
    return producto_db

def eliminar_producto(db: SessionDep, id: int) -> None:
    producto_db = db.get(Producto, id)
    if not producto_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    db.delete(producto_db)
    db.commit()