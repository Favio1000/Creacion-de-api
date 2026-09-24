from sqlalchemy import Column, Integer, String

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
