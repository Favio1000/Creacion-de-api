from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import schemas.schemas_ligas as schemas
from controller.controller_ligas import (
    actualizar_liga,
    crear_liga,
    eliminar_liga,
    listar_ligas,
)
from database.database import get_db

# Inicializamos el router con su prefijo y etiquetas para la documentación
router = APIRouter(prefix="/ligas", tags=["ligas"])


# 1. CREAR (POST)
#@app_post_en_router  
@router.post("/", response_model=schemas.LigaResponse)
def crear(liga: schemas.LigaCreate, db: Session = Depends(get_db)):  # noqa: B008
    return crear_liga(liga, db)


# 2. LEER TODOS (GET)
@router.get("/", response_model=list[schemas.LigaResponseConEquipos])
def mostrar_tabla(db: Session = Depends(get_db)):  # noqa: B008
    return listar_ligas(db)

# 3. ACTUALIZAR (PUT)
@router.put("/{liga_id}", response_model=schemas.LigaResponse)
def actualizar(
    liga_id: int, 
    liga_data: schemas.LigaUpdate, 
    db: Session = Depends(get_db)  # noqa: B008
):
    return actualizar_liga(liga_id, liga_data, db)

# 4. ELIMINAR (DELETE)
@router.delete("/{liga_id}", response_model=schemas.MensajeRespuesta)
def eliminar(liga_id: int, db: Session = Depends(get_db)):  # noqa: B008
    return eliminar_liga(liga_id, db)