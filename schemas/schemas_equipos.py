from pydantic import BaseModel


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