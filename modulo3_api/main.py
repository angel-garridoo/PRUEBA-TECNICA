from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from models import TareaCreate, TareaUpdate, Tarea, TokenResponse
from auth import verify_credentials, create_access_token, verify_token
import database as db

app = FastAPI(
    title="Mini API de Tareas",
    description="API REST con autenticación JWT para gestión de tareas",
    version="1.0.0"
)

@app.post("/auth/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    if not verify_credentials(form_data.username, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos"
        )
    token = create_access_token(form_data.username)
    return TokenResponse(access_token=token)


@app.get("/tasks", response_model=list[Tarea])
def list_tasks(current_user: str = Depends(verify_token)):

    return db.get_all_tasks()

@app.post("/tasks", response_model=Tarea, status_code=status.HTTP_201_CREATED)
def create_task(task: TareaCreate, current_user: str = Depends(verify_token)):

    new_task = db.create_task(
        titulo=task.titulo,
        descripcion=task.descripcion,
        estado=task.estado.value  
    )
    return new_task

@app.patch("/tasks/{task_id}", response_model=Tarea)
def update_task(
    task_id: int,
    task_update: TareaUpdate,
    current_user: str = Depends(verify_token)
):

    updated = db.update_task(task_id, task_update.estado.value)
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con id {task_id} no encontrada"
        )
    return updated

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, current_user: str = Depends(verify_token)):

    deleted = db.delete_task(task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con id {task_id} no encontrada"
        )
