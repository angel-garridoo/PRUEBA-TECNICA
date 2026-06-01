import pytest
from fastapi.testclient import TestClient
from main import app
import database as db

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_database():
    db.tasks_db.clear()  
    db.current_id = 0   

def get_valid_token() -> str:
    response = client.post("/auth/login", data={
        "username": "admin",
        "password": "1234"
    })
    return response.json()["access_token"]

def test_login_exitoso():
    response = client.post("/auth/login", data={
        "username": "admin",
        "password": "1234"
    })
    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert len(data["access_token"]) > 0
    assert data["token_type"] == "bearer"

def test_crear_tarea():
    token = get_valid_token()
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/tasks", json={
        "titulo": "Tarea de prueba",
        "descripcion": "Descripcion de prueba",
        "estado": "pendiente"
    }, headers=headers)

    assert response.status_code == 201  

    data = response.json()
    assert data["titulo"] == "Tarea de prueba"
    assert data["descripcion"] == "Descripcion de prueba"
    assert data["estado"] == "pendiente"
    assert "id" in data
    assert data["id"] == 1  


def test_rechazo_sin_token():
    response = client.get("/tasks")  
    assert response.status_code == 401
