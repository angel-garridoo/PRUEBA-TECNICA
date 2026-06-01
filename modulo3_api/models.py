from pydantic import BaseModel
from typing import Optional
from enum import Enum

class EstadoTarea(str, Enum):
    pendiente = "pendiente"
    en_progreso = "en_progreso"
    completado = "completado"

class TareaCreate(BaseModel):
    titulo: str  
    descripcion: str    
    estado: EstadoTarea = EstadoTarea.pendiente 

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

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"  