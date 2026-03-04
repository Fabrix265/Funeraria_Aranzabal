from fastapi import APIRouter, Depends, HTTPException, status, Query

from src.deps.db_session import SessionDep
from src.deps.role_check import get_current_admin, get_current_user
from src.deps.servicio_filters import filtros_servicio
from src.schemas.servicio import ServicioCrear, ServicioLeerCompleto, ServicioBase, ServicioPaginado
import src.services.servicio_service as service

servicio_router = APIRouter()


@servicio_router.get("/", response_model=ServicioPaginado)
def listar_servicios(
    session: SessionDep,
    filtros: dict = Depends(filtros_servicio),
    token: dict = Depends(get_current_user),
    offset: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(20, ge=1, le=100, description="Registros por página")
):
    return service.listar_servicios(
        session, 
        **filtros, 
        offset=offset, 
        limit=limit
    )

@servicio_router.get("/{servicio_id}", response_model=ServicioLeerCompleto)
def obtener_servicio(
    servicio_id: int,
    session: SessionDep,
    token: dict = Depends(get_current_user),
):
    return service.obtener_servicio(session, servicio_id)

@servicio_router.post("/", response_model=ServicioLeerCompleto, status_code=201)
def crear_servicio(
    datos: ServicioCrear,
    session: SessionDep,
    token: dict = Depends(get_current_user),
):

    id_usuario = token.get("id") or token.get("sub")

    if id_usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo extraer el ID del usuario del token. Revisa la clave 'id' o 'sub'."
        )

    try:
        id_usuario_int = int(id_usuario)
    except ValueError:
        raise HTTPException(status_code=400, detail="El ID de usuario en el token no es válido")

    return service.crear_servicio(session, datos, id_usuario_int)


@servicio_router.patch("/{servicio_id}", response_model=ServicioLeerCompleto)
def modificar_servicio(
    servicio_id: int,
    datos: ServicioBase,
    session: SessionDep,
    token: dict = Depends(get_current_admin),
):
    campos = datos.model_dump(exclude_unset=True)
    return service.modificar_servicio(session, servicio_id, campos)


@servicio_router.delete("/{servicio_id}")
def eliminar_servicio(
    servicio_id: int,
    session: SessionDep,
    token: dict = Depends(get_current_admin),
):
    return service.eliminar_servicio(session, servicio_id)