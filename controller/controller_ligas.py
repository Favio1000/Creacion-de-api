from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

import models.models_ligas as models
import schemas.schemas_ligas as schemas
from database.database import get_db


def crear_liga(liga: schemas.LigaCreate, db: Session = Depends(get_db)):  # noqa: B008
    # Verificar si la liga ya está registrado en la base de datos
    liga_existente = (
        db.query(models.LigaModel)
        .filter(models.LigaModel.nombre_liga == liga.nombre_liga)
        .first()
    )
    if liga_existente:
        raise HTTPException(
            status_code=400, detail="El nombre de la liga ya está registrado."
        )

    # Crear la instancia del modelo de SQLAlchemy con los datos validados de Pydantic
    nuevo_liga = models.LigaModel(
        nombre_liga=liga.nombre_liga, pais=liga.pais
    )
    try:
        # Guardar en la base de datos
        db.add(nuevo_liga)
        db.commit()
        db.refresh(nuevo_liga)  # Asigna el ID autoincremental generado por la BD

        return nuevo_liga
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fallo en la creacion de liga en el servidor {str(error)}" # noqa: RUF010
        )
    
    except SQLAlchemyError as err:  # noqa: B025
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Datos inválidos para la creación de la liga: {str(err)}" # noqa: RUF010
        )


def listar_ligas(db: Session = Depends(get_db)):  # noqa: B008
    ligas = db.query(models.LigaModel).all()
    return ligas

def actualizar_liga(
    liga_id: int, 
    liga_data: schemas.LigaUpdate, 
    db: Session = Depends(get_db)  # noqa: B008
):
    # 1. Buscar la liga que se desea modificar
    liga = (
        db.query(models.LigaModel)
        .filter(models.LigaModel.id == liga_id)
        .first()
    )
    if not liga:
        raise HTTPException(
            status_code=404, detail="Liga no encontrado para actualizar."
        )

    # 2. Verificar que el NUEVA liga no tenga el mismo nombre que otra liga
    nombre_duplicado = (
        db.query(models.LigaModel)
        .filter(models.LigaModel.nombre_liga == liga_data.nombre_liga)
        .filter(models.LigaModel.id != liga_id)  # Que no sea la misma liga
        .first()
    )
    if nombre_duplicado:
        raise HTTPException(
            status_code=400, detail="La liga ya está en uso ."
        )

    # 3. Modificar los datos del objeto en la base de datos
    liga.nombre_liga = liga_data.nombre_liga
    liga.pais = liga_data.pais
    try:
        # 4. Confirmar los cambios físicos en SQLite y refrescar datos
        db.commit()
        db.refresh(liga)

        return liga
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fallo en la actualizacion del servidor{str(error)}"  # noqa: RUF010
        )
    except SQLAlchemyError as err:  # noqa: B025
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Datos inválidos para la actualizacion de la liga: {str(err)}" # noqa: RUF010
        )
    

def eliminar_liga(liga_id: int, db: Session = Depends(get_db)):  # noqa: B008
    # 1. Buscar la liga en la base de datos
    liga = (
        db.query(models.LigaModel)
        .filter(models.LigaModel.id == liga_id)
        .first()
    )

    # 2. Si no existe, lanzar un error 404 (Not Found)
    if not liga:
        raise HTTPException(
            status_code=404, detail="La liga no existe o ya fue eliminado."
        )
    try:
        # 3. Si existe, decirle a SQLAlchemy que lo borre
        db.delete(liga)
        db.commit()  # Confirmar los cambios de forma física en SQLite

                # 4. Devolver un mensaje de éxito confirmado
        return {"message": f"Liga con ID {liga_id}con eliminado correctamente."}
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fallo en la eliminacion de liga en el servidor{str(error)}"  # noqa: RUF010
        )
    except SQLAlchemyError as err:  # noqa: B025
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Datos inválidos para la eliminacion de la liga: {str(err)}" # noqa: RUF010
            )
    