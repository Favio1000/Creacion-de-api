from fastapi import FastAPI

from database import Base, engine

# Importamos los módulos que acabamos de crear en la carpeta routers
from routers import tareas, usuarios

# 1. Crear las tablas físicas en SQLite al arrancar la aplicación
# Si el archivo 'sql_app.db' no existe, SQLAlchemy lo creará automáticamente con la tabla 'usuarios'
Base.metadata.create_all(bind=engine)

# 2. Inicializar la aplicación FastAPI
app = FastAPI(title="Mi API con FastAPI y SQLAlchemy")

# Conectamos las rutas secundarias a la aplicación principal
app.include_router(usuarios.router)
app.include_router(tareas.router)
