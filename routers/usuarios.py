from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

# Inicializamos el router con su prefijo y etiquetas para la documentación
router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


# 1. CREAR (POST)
#@app_post_en_router  
@router.post("/usuarios/", response_model=schemas.UsuarioResponse)
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


# 2. LEER TODOS (GET)
@router.get("/", response_model=list[schemas.UsuarioResponseConTareas])
def listar_usuarios(db: Session = Depends(get_db)):  # noqa: B008
    usuarios = db.query(models.UsuarioModel).all()
    return usuarios


# 3. ACTUALIZAR (PUT)
@router.put("/{usuario_id}", response_model=schemas.UsuarioResponse)
def actualizar_usuario(
    usuario_id: int, 
    usuario_data: schemas.UsuarioUpdate, 
    db: Session = Depends(get_db)  # noqa: B008
):
    # 1. Buscar al usuario que se desea modificar
    usuario = (
        db.query(models.UsuarioModel)
        .filter(models.UsuarioModel.id == usuario_id)
        .first()
    )
    if not usuario:
        raise HTTPException(
            status_code=404, detail="Usuario no encontrado para actualizar."
        )

    # 2. Verificar que el NUEVO email no pertenezca ya a OTRO usuario diferente
    email_duplicado = (
        db.query(models.UsuarioModel)
        .filter(models.UsuarioModel.email == usuario_data.email)
        .filter(models.UsuarioModel.id != usuario_id)  # Que no sea el mismo usuario
        .first()
    )
    if email_duplicado:
        raise HTTPException(
            status_code=400, detail="El correo electrónico ya está en uso por otro usuario."
        )

    # 3. Modificar los datos del objeto en la base de datos
    usuario.nombre = usuario_data.nombre
    usuario.email = usuario_data.email

    # 4. Confirmar los cambios físicos en SQLite y refrescar datos
    db.commit()
    db.refresh(usuario)

    return usuario


# 4. ELIMINAR (DELETE)
@router.delete("/{usuario_id}", response_model=schemas.MensajeRespuesta)
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):  # noqa: B008
    # 1. Buscar al usuario en la base de datos
    usuario = (
        db.query(models.UsuarioModel)
        .filter(models.UsuarioModel.id == usuario_id)
        .first()
    )

    # 2. Si no existe, lanzar un error 404 (Not Found)
    if not usuario:
        raise HTTPException(
            status_code=404, detail="El usuario no existe o ya fue eliminado."
        )

    # 3. Si existe, decirle a SQLAlchemy que lo borre
    db.delete(usuario)
    db.commit()  # Confirmar los cambios de forma física en SQLite

    # 4. Devolver un mensaje de éxito confirmado
    return {"message": f"Usuario con ID {usuario_id} eliminado correctamente."}
