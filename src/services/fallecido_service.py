from sqlmodel import Session, select
from fastapi import HTTPException, status
from src.models.fallecido import Fallecido

class FallecidoService:
    @staticmethod
    def listar_todos(session: Session) -> list[Fallecido]:
        return session.exec(select(Fallecido)).all()

    @staticmethod
    def obtener_por_id(session: Session, id: int) -> Fallecido:
        fallecido = session.get(Fallecido, id)
        if not fallecido:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Fallecido con ID {id} no encontrado"
            )
        return fallecido

    @staticmethod
    def actualizar(session: Session, id: int, datos: dict) -> Fallecido:
        fallecido = FallecidoService.obtener_por_id(session, id)
        for key, value in datos.items():
            setattr(fallecido, key, value)
        
        session.add(fallecido)
        session.commit()
        session.refresh(fallecido)
        return fallecido