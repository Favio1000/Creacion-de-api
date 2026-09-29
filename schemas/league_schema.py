from pydantic import BaseModel, Field

from schemas.team_schema import TeamResponse


# 1. Esquema Base: Define los campos comunes que toda liga siempre tendrá
class LeagueBase(BaseModel):
    league_name: str = Field(min_length=2, max_length=50)
    country: str = Field(min_length=2, max_length=30)

# 2. Esquema de Creación: Lo que el cliente envía cuando registra una liga
# Hereda de leagueBase, por lo que exige 'nombre' y 'pais' en el JSON de entrada
class LeagueCreate(LeagueBase):
    pass  # No necesitamos campos adicionales para crear


# Esquema para cuando se actualizan los datos de una liga (Petición PUT)
class LeagueUpdate(LeagueBase):
    pass  # Hereda nombre y pais. Si en el futuro quieres añadir campos opcionales, los pondrás aquí.


# 3. Esquema de Respuesta: Lo que la API le devolverá al cliente (JSON de salida)
# Incluye el 'id' que genera automáticamente la base de datos
class LeagueResponse(LeagueBase):
    id: int

    # Esta configuración es CRUCIAL para FastAPI y SQLAlchemy.
    # Le dice a Pydantic que pueda leer los datos directamente desde un objeto 
    # de SQLAlchemy (un modelo de base de datos) y transformarlo a JSON de forma automática.
    model_config = {
        "from_attributes": True
    }
# Esquema para mensajes genéricos de confirmación
class MessageResponse(BaseModel):
    message: str


# Modificamos la respuesta de ligas para que incluya su lista de Equipos de forma automática
class LeagueTeamsResponse(LeagueBase):
    id: int
    teams: list[TeamResponse] = (
        []
    )  # Si no tiene equipo, devolverá una lista vacía

    model_config = {"from_attributes": True}

