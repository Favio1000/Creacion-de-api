from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import schemas.league_schema as schemas
from controller.league_controller import (
    create_league,
    delete_league,
    list_league,
    update_league,
)
from database.database import get_db

# Inicializamos el router con su prefijo y etiquetas para la documentación
router = APIRouter(prefix="/leagues", tags=["Leagues"])


# 1. CREAR (POST)
#@app_post_en_router  
@router.post("/", response_model=schemas.LeagueResponse, status_code = status.HTTP_201_CREATED)
def create(league: schemas.LeagueCreate, db: Session = Depends(get_db)):  # noqa: B008
    return create_league(league, db)


# 2. LEER TODOS (GET)
@router.get("/", response_model=list[schemas.LeagueTeamsResponse])
def read(db: Session = Depends(get_db)):  # noqa: B008
    return list_league(db)

# 3. ACTUALIZAR (PUT)
@router.put("/{league_id}", response_model=schemas.LeagueResponse)
def update(
    league_id: int, 
    league_data: schemas.LeagueUpdate, 
    db: Session = Depends(get_db)  # noqa: B008
):
    return update_league(league_id, league_data, db)

# 4. ELIMINAR (DELETE)
@router.delete("/{league_id}", response_model=schemas.MessageResponse)
def delete (league_id: int, db: Session = Depends(get_db)):  # noqa: B008
    return delete_league(league_id, db)