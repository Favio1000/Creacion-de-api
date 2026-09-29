from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.database import Base


class LeagueModel(Base):
    # Nombre real que tendrá la tabla dentro de Base de datos
    __tablename__ = "leagues"

    # Clave primaria: autoincremental única para cada registro
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Nombre del liga (index=True agiliza las búsquedas por este campo)
    league_name = Column(String, unique=True, index=True)
    
    country = Column(String, index=True)

    # RELACIÓN: Un liga tiene muchos equipos.
    # 'back_populates' vincula este atributo con el del modelo TeamModel.
    # 'cascade' asegura que si borras una liga, se borren todas sus equipos automáticamente.
    teams = relationship(
        "TeamModel", back_populates="championship", cascade="all, delete-orphan"
    )


