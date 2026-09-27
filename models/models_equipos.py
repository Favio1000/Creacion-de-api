from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database.database import Base


class EquipoModel(Base):
    __tablename__ = "equipos"

    id = Column(Integer, primary_key=True, index=True)
    nombre_equipo = Column(String, index=True)
    ciudad = Column(String)
    # Conexión física a la tabla usuarios
    encargado_id = Column(Integer, ForeignKey("ligas.id"))

    # RELACIÓN: Cada tarea pertenece a un único autor
    encargado = relationship("LigaModel", back_populates="equipos")