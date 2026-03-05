# Funeraria_Aranzabal

## Activa el entorno virtual con:
`venv\Scripts\Activate.ps1`

## Para correrlo:
`uvicorn src.main:app`

## O para especificar un puerto(tiene que estar desactivado):
`uvicorn src.main:app --port 8000`

## Para correrlo escuchando(no para produccion):
`uvicorn src.main:app --port 8000 --reload`

## Para ver la documentacion:
`http://localhost:8000/docs`
`http://localhost:8000/redoc`

# API de Gestion Funeraria

Este sistema es una API robusta construida con FastAPI y SQLModel, disenada para gestionar el ciclo completo de servicios funebres, inventarios y roles de usuario.

## Caracteristicas Principales

- Paginacion Inteligente: Listado de servicios con conteo total para alto rendimiento.
- Gestion de Inventario Dinamico: Control de stock de ataudes y capillas con actualizaciones automaticas.
- Seguridad Basada en Roles: Diferenciacion clara entre Administradores y Trabajadores.
- Integridad de Datos: Eliminacion en cascada inteligente para mantener la base de datos limpia.

---

## Estructura del Proyecto y Flujos

### 1. Gestion de Servicios (`/servicios`)

Es el corazon del sistema. Al crear un servicio ocurre lo siguiente:

- Validacion de Stock: Verifica si hay ataudes y capillas disponibles.
- Deteccion de Personas: Si el fallecido o contratante ya existen (por DNI), los vincula; si no, los crea automaticamente.
- Descuento de Inventario: Resta automaticamente 1 unidad del stock de los productos asignados.
- Listado Paginado: El endpoint `GET /` devuelve un objeto estructurado:

```json
{ "total": 100, "offset": 0, "limit": 20, "data": [...] }
```

### 2. Modulos de Personas (`/fallecidos` y `/contratantes`)

Separados para permitir correcciones sin afectar la logica del servicio.

- Flujo: Los trabajadores pueden consultar datos, pero solo los Administradores pueden corregir nombres o DNIs mediante `PATCH`.
- Limpieza: Al eliminar un servicio, el sistema borra al fallecido y verifica si el contratante no tiene otros servicios activos para borrarlo tambien, evitando "datos fantasma".

### 3. Inventario (`/ataudes` y `/capillas`)

Control detallado de los insumos fisicos.

- Endpoints de Stock: Se implemento un acceso rapido `PATCH /{id}/stock` para sumar o restar existencias (entradas/salidas de almacen) sin riesgo de modificar precios o nombres por error.
- Regla de Negocio: El sistema bloquea cualquier venta o ajuste que resulte en stock negativo.

---

## Roles y Permisos

| Modulo      | Accion                      | Trabajador | Administrador |
|-------------|-----------------------------|------------|---------------|
| Servicios   | Crear / Ver                 | Si         | Si            |
| Servicios   | Modificar / Eliminar        | No         | Si            |
| Personas    | Corregir Datos (PATCH)      | No         | Si            |
| Inventario  | Ver Catalogo                | Si         | Si            |
| Inventario  | Ajustar Stock / Precios     | No         | Si            |

## Proximos Pasos Sugeridos

- Implementacion del modulo de machine learning para el futuro