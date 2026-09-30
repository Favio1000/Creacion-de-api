from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

import models.league_model as models
import schemas.league_schema as schemas
from database.database import get_db


def create_league(league: schemas.LeagueCreate, db: Session = Depends(get_db)):  # noqa: B008
    # Verificar si la liga ya está registrado en la base de datos
    league_exist = (
        db.query(models.LeagueModel)
        .filter(models.LeagueModel.league_name == league.league_name)
        .first()
    )
    if league_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de la liga ya está registrado."
        )

    # Crear la instancia del modelo de SQLAlchemy con los datos validados de Pydantic
    new_league = models.LeagueModel(
        league_name=league.league_name, country=league.country
    )
    try:
        # Guardar en la base de datos
        db.add(new_league)
        db.commit()
        db.refresh(new_league)  # Asigna el ID autoincremental generado por la BD

        return new_league
    
    except SQLAlchemyError as error:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Fallo en la creacion de liga en el servidor:{str(error)}"  # noqa: RUF010
            )

def list_league(db: Session = Depends(get_db)):  # noqa: B008
    league = db.query(models.LeagueModel).all()
    return league

def update_league(
    league_id: int, 
    league_data: schemas.LeagueUpdate, 
    db: Session = Depends(get_db)  # noqa: B008
):
    # 1. Buscar la liga que se desea modificar
    league = (
        db.query(models.LeagueModel)
        .filter(models.LeagueModel.id == league_id)
        .first()
    )
    if not league:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Liga no encontrada para actualizar."
        )

    # 2. Verificar que el NUEVA liga no tenga el mismo nombre que otra liga
    duplicate_name = (
        db.query(models.LeagueModel)
        .filter(models.LeagueModel.league_name == league_data.league_name)
        .filter(models.LeagueModel.id != league_id)  # Que no sea la misma liga
        .first()
    )
    if duplicate_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La liga ya está en uso ."
        )

    # 3. Modificar los datos del objeto en la base de datos
    league.league_name = league_data.league_name
    league.country = league_data.country
    try:
        # 4. Confirmar los cambios físicos en SQLite y refrescar datos
        db.commit()
        db.refresh(league)

        return league
    
    except SQLAlchemyError as error:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Fallo en la actualizacion del servidor{str(error)}"  # noqa: RUF010
            )
    

def delete_league(league_id: int, db: Session = Depends(get_db)):  # noqa: B008
    # 1. Buscar la liga en la base de datos
    league = (
        db.query(models.LeagueModel)
        .filter(models.LeagueModel.id == league_id)
        .first()
    )

    # 2. Si no existe, lanzar un error 404 (Not Found)
    if not league:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="La liga no existe o ya fue eliminado."
        )
    try:
        # 3. Si existe, decirle a SQLAlchemy que lo borre
        db.delete(league)
        db.commit()  # Confirmar los cambios de forma física en SQLite

                # 4. Devolver un mensaje de éxito confirmado
        return {"message": f"Liga con ID {league_id} eliminado correctamente."}
    
    
    except SQLAlchemyError as error:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Fallo en la actualizacion del servidor{str(error)}"  # noqa: RUF010
            )
    