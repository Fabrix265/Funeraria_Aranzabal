from sqlmodel import Session, select
from fastapi import HTTPException, status
from src.models.contratante import Contratante

class ContratanteService:
    @staticmethod
    def listar_todos(session: Session) -> list[Contratante]:
        return session.exec(select(Contratante)).all()

    @staticmethod
    def obtener_por_id(session: Session, id: int) -> Contratante:
        contratante = session.get(Contratante, id)
        if not contratante:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Contratante con ID {id} no encontrado"
            )
        return contratante

    @staticmethod
    def actualizar(session: Session, id: int, datos: dict) -> Contratante:
        contratante = ContratanteService.obtener_por_id(session, id)
        for key, value in datos.items():
            setattr(contratante, key, value)
            
        session.add(contratante)
        session.commit()
        session.refresh(contratante)
        return contratante