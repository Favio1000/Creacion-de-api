from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

router = APIRouter(tags=["Equipos"])


# 1. CREAR TAREA PARA UN USUARIO
@router.post(
    "/ligas/{liga_id}/equipos/", response_model=schemas.EquipoResponse
)
def crear_equipo_para_liga(
    liga_id: int,
    equipo: schemas.EquipoCreate,
    db: Session = Depends(get_db),  # noqa: B008
):
    # Verificar primero si el usuario dueño de la tarea existe
    liga_existe = (
        db.query(models.LigaModel)
        .filter(models.LigaModel.id == liga_id)
        .first()
    )
    if not liga_existe:
        raise HTTPException(
            status_code=404, detail="Liga no encontrado para asignarle la equipo."
        )

    # Crear la tarea extrayendo los datos del JSON y amarrando el autor_id de la URL
    nueva_equipo = models.EquipoModel(**equipo.model_dump(), encargado_id=liga_id)

    db.add(nueva_equipo)
    db.commit()
    db.refresh(nueva_equipo)

    return nueva_equipo


# 2. LEER TODAS LAS TAREAS GENERALES
@router.get("/equipos/", response_model=list[schemas.EquipoResponse])
def listar_equipos(db: Session = Depends(get_db)):  # noqa: B008
    return db.query(models.EquipoModel).all()
