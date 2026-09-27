from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import schemas.schemas_equipos as schemas
from controller.controller_equipos import crear_equipo_para_liga, listar_equipos
from database.database import get_db

router = APIRouter(tags=["Equipos"])


# 1. CREAR TAREA PARA UN USUARIO
@router.post(
    "/ligas/{liga_id}/equipos/", response_model=schemas.EquipoResponse
)
def crear(
    liga_id: int,
    equipo: schemas.EquipoCreate,
    db: Session = Depends(get_db),  # noqa: B008
):
    return crear_equipo_para_liga(liga_id, equipo, db)


# 2. LEER TODAS LAS TAREAS GENERALES
@router.get("/equipos/", response_model=list[schemas.EquipoResponse])
def mostrar(db: Session = Depends(get_db)):  # noqa: B008
    return listar_equipos(db)
