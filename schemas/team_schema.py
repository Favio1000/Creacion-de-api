from pydantic import BaseModel, Field


# Campos comunes para crear/leer equipo
class TeamBase(BaseModel):
    team_name: str = Field(min_length=2, max_length=50)
    city: str = Field(min_length=2, max_length=30)


# Lo que el cliente envía al crear un equipo
class TeamCreate(TeamBase):
    pass

class TeamUpdate(TeamBase):
    pass

# Lo que la API devuelve al consultar un equipo
class TeamResponse(TeamBase):
    id: int
    championship_id: int

    model_config = {"from_attributes": True}

# Esquema para mensajes genéricos de confirmación
class MessageTeamResponse(BaseModel):
    message: str