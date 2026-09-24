from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

router = APIRouter(tags=["Tareas"])


# 1. CREAR TAREA PARA UN USUARIO
@router.post(
    "/usuarios/{usuario_id}/tareas/", response_model=schemas.TareaResponse
)
def crear_tarea_para_usuario(
    usuario_id: int,
    tarea: schemas.TareaCreate,
    db: Session = Depends(get_db),  # noqa: B008
):
    # Verificar primero si el usuario dueño de la tarea existe
    usuario_existe = (
        db.query(models.UsuarioModel)
        .filter(models.UsuarioModel.id == usuario_id)
        .first()
    )
    if not usuario_existe:
        raise HTTPException(
            status_code=404, detail="Usuario no encontrado para asignarle la tarea."
        )

    # Crear la tarea extrayendo los datos del JSON y amarrando el autor_id de la URL
    nueva_tarea = models.TareaModel(**tarea.model_dump(), autor_id=usuario_id)

    db.add(nueva_tarea)
    db.commit()
    db.refresh(nueva_tarea)

    return nueva_tarea


# 2. LEER TODAS LAS TAREAS GENERALES
@router.get("/tareas/", response_model=list[schemas.TareaResponse])
def listar_tareas(db: Session = Depends(get_db)):  # noqa: B008
    return db.query(models.TareaModel).all()
