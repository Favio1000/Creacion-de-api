from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class UsuarioModel(Base):
    # Nombre real que tendrá la tabla dentro de SQLite
    __tablename__ = "usuarios"

    # Clave primaria: autoincremental única para cada registro
    id = Column(Integer, primary_key=True, index=True)
    
    # Nombre del usuario (index=True agiliza las búsquedas por este campo)
    nombre = Column(String, index=True)
    
    # Email único: SQLite arrojará un error si se intenta repetir un email
    email = Column(String, unique=True, index=True)

    # RELACIÓN: Un usuario tiene muchas tareas.
    # 'back_populates' vincula este atributo con el del modelo TareaModel.
    # 'cascade' asegura que si borras un usuario, se borren todas sus tareas automáticamente.
    tareas = relationship(
        "TareaModel", back_populates="autor", cascade="all, delete-orphan"
    )


class TareaModel(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    descripcion = Column(String)
    # Conexión física a la tabla usuarios
    autor_id = Column(Integer, ForeignKey("usuarios.id"))

    # RELACIÓN: Cada tarea pertenece a un único autor
    autor = relationship("UsuarioModel", back_populates="tareas")