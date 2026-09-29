from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
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
    # Verificar primero si algun el equipo ya esta registrado en otra liga existe
    liga_existe = (
        db.query(LigaModel)
        .filter(LigaModel.id == liga_id)
        .first()
    )
    if not liga_existe:
        raise HTTPException(
            status_code=404, detail="Liga no encontrado para asignarle la equipo."
        )

    # Crear el equipo extrayendo los datos del JSON y amarrando el liga_id de la URL
    nueva_equipo = EquipoModel(**equipo.model_dump(), encargado_id=liga_id)
    try:
        db.add(nueva_equipo)
        db.commit()
        db.refresh(nueva_equipo)

        return nueva_equipo
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fallo en la eliminacion de liga {str(error)}"  # noqa: RUF010
        )

def listar_equipos(db: Session = Depends(get_db)):  # noqa: B008
    return db.query(EquipoModel).all()