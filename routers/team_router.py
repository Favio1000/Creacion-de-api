from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import schemas.team_schema as schema
from controller.team_controller import create_team, delete_team, list_team, update_team
from database.database import get_db

router = APIRouter(tags=["Teams"])


# 1. CREAR EQUIPO
@router.post(
    "/leagues/{league_id}/teams/", response_model=schema.TeamResponse, status_code=status.HTTP_201_CREATED
)
def create(
    league_id: int,
    team: schema.TeamCreate,
    db: Session = Depends(get_db),  # noqa: B008
):
    return create_team(league_id, team, db)


# 2. LEER TODAS LA LISTA DE EQUIPOS
@router.get("/teams/", response_model=list[schema.TeamResponse])
def read(db: Session = Depends(get_db)):  # noqa: B008
    return list_team(db)

# 3. ACTUALIZAR (PUT)
@router.put("/teams/{team_id}", response_model=schema.TeamResponse)
def update(
    team_id: int, 
    team_data: schema.TeamUpdate, 
    db: Session = Depends(get_db)  # noqa: B008
):
    return update_team(team_id, team_data, db)

# 4. ELIMINAR (DELETE)
@router.delete("/teams/{team_id}", response_model=schema.MessageTeamResponse)
def delete (team_id: int, db: Session = Depends(get_db)):  # noqa: B008
    return delete_team(team_id, db)