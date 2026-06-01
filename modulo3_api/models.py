from pydantic import BaseModel
from enum import Enum


# Estados validos que acepta la API para una tarea.
class EstadoTarea(str, Enum):
    pendiente = "pendiente"
    en_progreso = "en_progreso"
    completado = "completado"


# Datos que se necesitan para crear una tarea.
class TareaCreate(BaseModel):
    titulo: str
    descripcion: str
    estado: EstadoTarea = EstadoTarea.pendiente


# Para actualizar una tarea solo se permite cambiar el estado.
class TareaUpdate(BaseModel):
    estado: EstadoTarea


class Tarea(BaseModel):
    id: int
    titulo: str
    descripcion: str
    estado: EstadoTarea


class LoginRequest(BaseModel):
    username: str
    password: str


# Respuesta estandar del login cuando se genera un JWT valido.
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
