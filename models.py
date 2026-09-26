from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class LigaModel(Base):
    # Nombre real que tendrá la tabla dentro de SQLite
    __tablename__ = "ligas"

    # Clave primaria: autoincremental única para cada registro
    id = Column(Integer, primary_key=True, index=True)
    
    # Nombre del usuario (index=True agiliza las búsquedas por este campo)
    nombre_liga = Column(String, index=True)
    
    # Email único: SQLite arrojará un error si se intenta repetir un email
    pais = Column(String, unique=True, index=True)

    # RELACIÓN: Un usuario tiene muchas tareas.
    # 'back_populates' vincula este atributo con el del modelo TareaModel.
    # 'cascade' asegura que si borras un usuario, se borren todas sus tareas automáticamente.
    equipos = relationship(
        "EquipoModel", back_populates="encargado", cascade="all, delete-orphan"
    )


class EquipoModel(Base):
    __tablename__ = "equipos"

    id = Column(Integer, primary_key=True, index=True)
    nombre_equipo = Column(String, index=True)
    ciudad = Column(String)
    # Conexión física a la tabla usuarios
    encargado_id = Column(Integer, ForeignKey("ligas.id"))

    # RELACIÓN: Cada tarea pertenece a un único autor
    encargado = relationship("LigaModel", back_populates="equipos")