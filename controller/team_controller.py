from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

import schemas.team_schema as schemas
from database.database import get_db
from models.league_model import LeagueModel
from models.team_model import TeamModel


def create_team(
    league_id: int,
    team: schemas.TeamCreate,
    db: Session = Depends(get_db),  # noqa: B008
):
    # Verificar primero si algun el equipo ya esta registrado en otra liga existe
    league_exists = (
        db.query(LeagueModel)
        .filter(LeagueModel.id == league_id)
        .first()
    )
    if not league_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Liga no encontrado para asignarle la equipo."
        )

    # Crear el equipo extrayendo los datos del JSON y amarrando el liga_id de la URL
    new_team = TeamModel(**team.model_dump(), championship_id=league_id)
    try:
        db.add(new_team)
        db.commit()
        db.refresh(new_team)

        return new_team
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fallo en la creacion del equipo en el servidor {str(error)}"  # noqa: RUF010
        )
    
    
def list_team(db: Session = Depends(get_db)):  # noqa: B008
    return db.query(TeamModel).all()


def update_team(
    team_id: int, 
    team_data: schemas.TeamUpdate, 
    db: Session = Depends(get_db)  # noqa: B008
):
    # 1. Buscar la liga que se desea modificar
    team = (
        db.query(TeamModel)
        .filter(TeamModel.id == team_id)
        .first()
    )
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Equipo no encontrado para actualizar."
        )

    # 2. Verificar que el NUEVA liga no tenga el mismo nombre que otra liga
    duplicate_name = (
        db.query(TeamModel)
        .filter(TeamModel.team_name == team_data.team_name)
        .filter(TeamModel.id != team_id)  # Que no sea la misma liga
        .first()
    )
    if duplicate_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La equipo ya está en uso ."
        )

    # 3. Modificar los datos del objeto en la base de datos
    team.team_name = team_data.team_name
    team.city = team_data.city
    try:
        # 4. Confirmar los cambios físicos en SQLite y refrescar datos
        db.commit()
        db.refresh(team)

        return team
    
    except SQLAlchemyError as error:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Fallo de la actualizacion del equpo en el servidor{str(error)}"  # noqa: RUF010
            )
    

def delete_team(team_id: int, db: Session = Depends(get_db)):  # noqa: B008
    # 1. Buscar la liga en la base de datos
    team = (
        db.query(TeamModel)
        .filter(TeamModel.id == team_id)
        .first()
    )

    # 2. Si no existe, lanzar un error 404 (Not Found)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="La liga no existe o ya fue eliminado."
        )
    try:
        # 3. Si existe, decirle a SQLAlchemy que lo borre
        db.delete(team)
        db.commit()  # Confirmar los cambios de forma física en SQLite

                # 4. Devolver un mensaje de éxito confirmado
        return {"message": f"Equipo con ID {team_id} eliminado correctamente."}
    
    
    except SQLAlchemyError as error:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Fallo en la actualizacion del servidor{str(error)}"  # noqa: RUF010
            )
  