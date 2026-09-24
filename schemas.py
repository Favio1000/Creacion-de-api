from pydantic import BaseModel


# 1. Esquema Base: Define los campos comunes que todo Usuario siempre tendrá
class UsuarioBase(BaseModel):
    nombre: str
    email: str

# 2. Esquema de Creación: Lo que el cliente envía cuando registra un usuario
# Hereda de UsuarioBase, por lo que exige 'nombre' y 'email' en el JSON de entrada
class UsuarioCreate(UsuarioBase):
    pass  # No necesitamos campos adicionales para crear


# Esquema para cuando se actualizan los datos de un usuario (Petición PUT)
class UsuarioUpdate(UsuarioBase):
    pass  # Hereda nombre y email. Si en el futuro quieres añadir campos opcionales, los pondrás aquí.


# 3. Esquema de Respuesta: Lo que la API le devolverá al cliente (JSON de salida)
# Incluye el 'id' que genera automáticamente la base de datos
class UsuarioResponse(UsuarioBase):
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
