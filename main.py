from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine

# Importamos los módulos que acabamos de crear en la carpeta routers
from routers import equipos, ligas

# 1. Crear las tablas físicas en SQLite al arrancar la aplicación
# Si el archivo 'sql_app.db' no existe, SQLAlchemy lo creará automáticamente con la tabla 'usuarios'
Base.metadata.create_all(bind=engine)

# 2. Inicializar la aplicación FastAPI
app = FastAPI(title="Mi API con FastAPI y SQLAlchemy")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Conectamos las rutas secundarias a la aplicación principal
app.include_router(ligas.router)
app.include_router(equipos.router)


