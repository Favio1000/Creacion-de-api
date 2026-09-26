from pydantic import BaseModel


# 1. Esquema Base: Define los campos comunes que todo Usuario siempre tendrá
class LigaBase(BaseModel):
    nombre_liga: str
    pais: str

# 2. Esquema de Creación: Lo que el cliente envía cuando registra un usuario
# Hereda de UsuarioBase, por lo que exige 'nombre' y 'email' en el JSON de entrada
class LigaCreate(LigaBase):
    pass  # No necesitamos campos adicionales para crear


# Esquema para cuando se actualizan los datos de un usuario (Petición PUT)
class LigaUpdate(LigaBase):
    pass  # Hereda nombre y email. Si en el futuro quieres añadir campos opcionales, los pondrás aquí.


# 3. Esquema de Respuesta: Lo que la API le devolverá al cliente (JSON de salida)
# Incluye el 'id' que genera automáticamente la base de datos
class LigaResponse(LigaBase):
    id: int

    # Esta configuración es CRUCIAL para FastAPI y SQLAlchemy.
    # Le dice a Pydantic que pueda leer los datos directamente desde un objeto 
    # de SQLAlchemy (un modelo de base de datos) y transformarlo a JSON de forma automática.
    model_config = {
        "from_attributes": True
    }
# Esquema para mensajes genéricos de confirmación
class MensajeRespuesta(BaseModel):
    message: str

# --- ESQUEMAS DE TAREAS ---


# Campos comunes para crear/leer tareas
class EquipoBase(BaseModel):
    nombre_equipo: str
    ciudad: str


# Lo que el cliente envía al crear una tarea
class EquipoCreate(EquipoBase):
    pass


# Lo que la API devuelve al consultar una tarea
class EquipoResponse(EquipoBase):
    id: int
    encargado_id: int

    model_config = {"from_attributes": True}


# --- ACTUALIZACIÓN DEL ESQUEMA DE USUARIO ---
# Modificamos la respuesta de usuario para que incluya su lista de Equipos de forma automática
class LigaResponseConEquipos(LigaBase):
    id: int
    equipos: list[EquipoResponse] = (
        []
    )  # Si no tiene tareas, devolverá una lista vacía

    model_config = {"from_attributes": True}

