from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

# Inicializamos el router con su prefijo y etiquetas para la documentación
router = APIRouter(prefix="/ligas", tags=["ligas"])


# 1. CREAR (POST)
#@app_post_en_router  
@router.post("/", response_model=schemas.LigaResponse)
def crear_liga(liga: schemas.LigaCreate, db: Session = Depends(get_db)):  # noqa: B008
    # Verificar si el email ya está registrado en la base de datos
    liga_existente = (
        db.query(models.LigaModel)
        .filter(models.LigaModel.pais == liga.pais)
        .first()
    )
    if liga_existente:
        raise HTTPException(
            status_code=400, detail="El correo electrónico ya está registrado."
        )

    # Crear la instancia del modelo de SQLAlchemy con los datos validados de Pydantic
    nuevo_liga = models.LigaModel(
        nombre_liga=liga.nombre_liga, pais=liga.pais
    )

    # Guardar en la base de datos
    db.add(nuevo_liga)
    db.commit()
    db.refresh(nuevo_liga)  # Asigna el ID autoincremental generado por la BD

    return nuevo_liga


# 2. LEER TODOS (GET)
@router.get("/", response_model=list[schemas.LigaResponseConEquipos])
def listar_ligas(db: Session = Depends(get_db)):  # noqa: B008
    ligas = db.query(models.LigaModel).all()
    return ligas


# 3. ACTUALIZAR (PUT)
@router.put("/{liga_id}", response_model=schemas.LigaResponse)
def actualizar_liga(
    liga_id: int, 
    liga_data: schemas.LigaUpdate, 
    db: Session = Depends(get_db)  # noqa: B008
):
    # 1. Buscar al usuario que se desea modificar
    liga = (
        db.query(models.LigaModel)
        .filter(models.LigaModel.id == liga_id)
        .first()
    )
    if not liga:
        raise HTTPException(
            status_code=404, detail="Liga no encontrado para actualizar."
        )

    # 2. Verificar que el NUEVO email no pertenezca ya a OTRO usuario diferente
    pais_duplicado = (
        db.query(models.LigaModel)
        .filter(models.LigaModel.pais == liga_data.pais)
        .filter(models.LigaModel.id != liga_id)  # Que no sea el mismo usuario
        .first()
    )
    if pais_duplicado:
        raise HTTPException(
            status_code=400, detail="El correo electrónico ya está en uso por otro liga."
        )

    # 3. Modificar los datos del objeto en la base de datos
    liga.nombre_liga = liga_data.nombre_liga
    liga.pais = liga_data.pais

    # 4. Confirmar los cambios físicos en SQLite y refrescar datos
    db.commit()
    db.refresh(liga)

    return liga


# 4. ELIMINAR (DELETE)
@router.delete("/{liga_id}", response_model=schemas.MensajeRespuesta)
def eliminar_liga(liga_id: int, db: Session = Depends(get_db)):  # noqa: B008
    # 1. Buscar al usuario en la base de datos
    liga = (
        db.query(models.LigaModel)
        .filter(models.LigaModel.id == liga_id)
        .first()
    )

    # 2. Si no existe, lanzar un error 404 (Not Found)
    if not liga:
        raise HTTPException(
            status_code=404, detail="El liga no existe o ya fue eliminado."
        )

    # 3. Si existe, decirle a SQLAlchemy que lo borre
    db.delete(liga)
    db.commit()  # Confirmar los cambios de forma física en SQLite

    # 4. Devolver un mensaje de éxito confirmado
    return {"message": f"Liga con ID {liga_id} eliminado correctamente."}
