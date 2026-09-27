from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import schemas.schemas_equipos as schemas
from database.database import get_db
from models.models_equipos import EquipoModel
from models.models_ligas import LigaModel


def crear_equipo_para_liga(
    liga_id: int,
    equipo: schemas.EquipoCreate,
    db: Session = Depends(get_db),  # noqa: B008
):
    # Verificar primero si el usuario dueño de la tarea existe
    liga_existe = (
        db.query(LigaModel)
        .filter(LigaModel.id == liga_id)
        .first()
    )
    if not liga_existe:
        raise HTTPException(
            status_code=404, detail="Liga no encontrado para asignarle la equipo."
        )

    # Crear la tarea extrayendo los datos del JSON y amarrando el autor_id de la URL
    nueva_equipo = EquipoModel(**equipo.model_dump(), encargado_id=liga_id)

    db.add(nueva_equipo)
    db.commit()
    db.refresh(nueva_equipo)

    return nueva_equipo

def listar_equipos(db: Session = Depends(get_db)):  # noqa: B008
    return db.query(EquipoModel).all()