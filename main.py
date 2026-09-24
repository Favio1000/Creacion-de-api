from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import Base, engine, get_db

# 1. Crear las tablas físicas en SQLite al arrancar la aplicación
# Si el archivo 'sql_app.db' no existe, SQLAlchemy lo creará automáticamente con la tabla 'usuarios'
Base.metadata.create_all(bind=engine)

# 2. Inicializar la aplicación FastAPI
app = FastAPI(title="Mi API con FastAPI y SQLAlchemy")


# 3. Endpoint para CREAR un usuario (POST)
@app.post("/usuarios/", response_model=schemas.UsuarioResponse)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):  # noqa: B008
    # Verificar si el email ya está registrado en la base de datos
    usuario_existente = (
        db.query(models.UsuarioModel)
        .filter(models.UsuarioModel.email == usuario.email)
        .first()
    )
    if usuario_existente:
        raise HTTPException(
            status_code=400, detail="El correo electrónico ya está registrado."
        )

    # Crear la instancia del modelo de SQLAlchemy con los datos validados de Pydantic
    nuevo_usuario = models.UsuarioModel(
        nombre=usuario.nombre, email=usuario.email
    )

    # Guardar en la base de datos
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)  # Asigna el ID autoincremental generado por la BD

    return nuevo_usuario


# 4. Endpoint para OBTENER todos los usuarios (GET)
@app.get("/usuarios/", response_model=list[schemas.UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):  # noqa: B008
    usuarios = db.query(models.UsuarioModel).all()
    return usuarios
