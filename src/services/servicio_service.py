from sqlmodel import Session, delete, select, or_, func
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from datetime import date
from typing import Optional

from src.models.servicio import Servicio
from src.models.servicio_vehiculo import ServicioVehiculo
from src.models.fallecido import Fallecido
from src.models.contratante import Contratante
from src.models.ataud import Ataud
from src.models.capilla import Capilla
from src.models.vehiculo import Vehiculo
from src.schemas.servicio import ServicioCrear


def _get_servicio_completo(session: Session, servicio_id: int) -> Servicio:
    statement = (
        select(Servicio)
        .where(Servicio.id == servicio_id)
        .options(
            selectinload(Servicio.fallecido),
            selectinload(Servicio.contratante),
            selectinload(Servicio.ataud),
            selectinload(Servicio.capilla),
            selectinload(Servicio.vehiculos_asignados).selectinload(ServicioVehiculo.vehiculo),
        )
    )
    servicio = session.exec(statement).first()
    if not servicio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Servicio con id {servicio_id} no encontrado"
        )
    return servicio


def listar_servicios(
    session: Session,
    fecha: Optional[date] = None,
    nombre: Optional[str] = None,
    dni: Optional[str] = None,
    telefono: Optional[str] = None,
    offset: int = 0,
    limit: int = 20
) -> dict: 
    
    base_query = (
        select(Servicio)
        .join(Contratante, Servicio.id_contratante == Contratante.id)
        .join(Fallecido, Servicio.id_fallecido == Fallecido.id)
    )

    if fecha:
        base_query = base_query.where(Servicio.fecha == fecha)
    if nombre:
        nombre_like = f"%{nombre}%"
        base_query = base_query.where(or_(
            Contratante.nombre.ilike(nombre_like),
            Fallecido.nombre.ilike(nombre_like)
        ))
    if dni:
        base_query = base_query.where(or_(
            Contratante.dni == dni,
            Fallecido.dni == dni
        ))
    if telefono:
        base_query = base_query.where(Contratante.telefono == telefono)

    total_query = select(func.count()).select_from(base_query.subquery())
    total = session.exec(total_query).one()

    statement = (
        base_query
        .options(
            selectinload(Servicio.fallecido),
            selectinload(Servicio.contratante),
            selectinload(Servicio.ataud),
            selectinload(Servicio.capilla),
            selectinload(Servicio.vehiculos_asignados).selectinload(ServicioVehiculo.vehiculo),
        )
        .offset(offset)
        .limit(limit)
    )
    
    resultados = session.exec(statement).all()

    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "data": resultados
    }

def obtener_servicio(session: Session, servicio_id: int) -> Servicio:
    return _get_servicio_completo(session, servicio_id)


def crear_servicio(session: Session, datos: ServicioCrear, id_usuario: int) -> Servicio:
    try:
        capilla = session.get(Capilla, datos.id_capilla)
        if not capilla:
            raise HTTPException(status_code=404, detail="Capilla no encontrada")
        if capilla.stock <= 0:
            raise HTTPException(status_code=400, detail="No hay stock de capilla")

        ataud = None
        if datos.id_ataud is not None:
            ataud = session.get(Ataud, datos.id_ataud)
            if not ataud:
                raise HTTPException(status_code=404, detail="Ataúd no encontrado")
            if ataud.stock <= 0:
                raise HTTPException(status_code=400, detail="No hay stock de ataúd")

        vehiculos = []
        for id_v in datos.ids_vehiculos:
            v = session.get(Vehiculo, id_v)
            if not v:
                raise HTTPException(status_code=404, detail=f"Vehículo {id_v} no encontrado")
            vehiculos.append(v)

        contratante = session.exec(
            select(Contratante).where(Contratante.dni == datos.contratante.dni)
        ).first()
        if not contratante:
            contratante = Contratante(**datos.contratante.model_dump())
            session.add(contratante)
            session.flush()

        fallecido = session.exec(
            select(Fallecido).where(Fallecido.dni == datos.fallecido.dni)
        ).first()
        if fallecido:
            existente = session.exec(select(Servicio).where(Servicio.id_fallecido == fallecido.id)).first()
            if existente:
                raise HTTPException(status_code=400, detail="El fallecido ya tiene un servicio registrado")
        else:
            fallecido = Fallecido(**datos.fallecido.model_dump())
            session.add(fallecido)
            session.flush()

        servicio = Servicio(
            id_usuario=id_usuario,
            id_ataud=datos.id_ataud,
            id_capilla=datos.id_capilla,
            id_contratante=contratante.id,
            id_fallecido=fallecido.id,
            direccion_velacion=datos.direccion_velacion,
            tipo_pago=datos.tipo_pago,
            arreglo_flora=datos.arreglo_flora,
            fecha=datos.fecha,
            cantidad_cargadores=datos.cantidad_cargadores,
            director_sepelio=datos.director_sepelio,
        )
        session.add(servicio)
        session.flush()

        for v in vehiculos:
            sv = ServicioVehiculo(id_servicio=servicio.id, id_vehiculo=v.id)
            session.add(sv)

        capilla.stock -= 1
        if ataud:
            ataud.stock -= 1

        session.commit()
        return _get_servicio_completo(session, servicio.id)

    except HTTPException as he:
        session.rollback()
        raise he
    except Exception as e:
        session.rollback()
        print(f"ERROR CRÍTICO EN SERVICE: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


def modificar_servicio(
    session: Session,
    servicio_id: int,
    datos: dict,
) -> Servicio:
    servicio = session.get(Servicio, servicio_id)
    if not servicio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Servicio con id {servicio_id} no encontrado"
        )

    if "id_capilla" in datos and datos["id_capilla"] != servicio.id_capilla:
        nueva_capilla = session.get(Capilla, datos["id_capilla"])
        if not nueva_capilla:
            raise HTTPException(status_code=404, detail="Nueva capilla no encontrada")
        if nueva_capilla.stock <= 0:
            raise HTTPException(status_code=400, detail="No hay stock en la nueva capilla")
        capilla_anterior = session.get(Capilla, servicio.id_capilla)
        if capilla_anterior:
            capilla_anterior.stock += 1
        nueva_capilla.stock -= 1

    if "id_ataud" in datos and datos["id_ataud"] != servicio.id_ataud:
        if servicio.id_ataud is not None:
            ataud_anterior = session.get(Ataud, servicio.id_ataud)
            if ataud_anterior:
                ataud_anterior.stock += 1
        if datos["id_ataud"] is not None:
            nuevo_ataud = session.get(Ataud, datos["id_ataud"])
            if not nuevo_ataud:
                raise HTTPException(status_code=404, detail="Nuevo ataúd no encontrado")
            if nuevo_ataud.stock <= 0:
                raise HTTPException(status_code=400, detail="No hay stock en el nuevo ataúd")
            nuevo_ataud.stock -= 1

    for campo, valor in datos.items():
        setattr(servicio, campo, valor)

    session.add(servicio)
    session.commit()
    return _get_servicio_completo(session, servicio_id)


def eliminar_servicio(session: Session, servicio_id: int) -> dict:
    servicio = session.get(Servicio, servicio_id)
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    id_fallecido = servicio.id_fallecido
    id_contratante = servicio.id_contratante

    capilla = session.get(Capilla, servicio.id_capilla)
    if capilla:
        capilla.stock += 1

    if servicio.id_ataud:
        ataud = session.get(Ataud, servicio.id_ataud)
        if ataud:
            ataud.stock += 1

    session.exec(
        delete(ServicioVehiculo).where(ServicioVehiculo.id_servicio == servicio_id)
    )

    session.delete(servicio)
    session.flush()

    fallecido = session.get(Fallecido, id_fallecido)
    if fallecido:
        session.delete(fallecido)

    otros_servicios = session.exec(
        select(Servicio).where(Servicio.id_contratante == id_contratante)
    ).first()
    if not otros_servicios:
        contratante = session.get(Contratante, id_contratante)
        if contratante:
            session.delete(contratante)

    session.commit()
    return {"message": f"Servicio {servicio_id} eliminado exitosamente y stocks actualizados"}