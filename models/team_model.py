from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database.database import Base


class TeamModel(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    team_name = Column(String, index=True)
    city = Column(String)
    # Conexión física a la tabla equipos
    championship_id = Column(Integer, ForeignKey("leagues.id"))

    # RELACIÓN: Cada equipo pertenece a un única liga
    championship = relationship("LeagueModel", back_populates="teams")