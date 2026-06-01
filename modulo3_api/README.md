# Mini API de Tareas

API REST sencilla para gestionar tareas. Incluye autenticacion con JWT, rutas protegidas y pruebas automaticas con `pytest`.

El proyecto esta pensado como una API pequena pero completa: permite iniciar sesion, obtener un token, crear tareas, listarlas, actualizar su estado y eliminarlas.

## Requisitos

- Python 3.11 o superior
- `pip`

## Instalacion

Desde la raiz del repositorio:

```bash
cd modulo3_api
pip install -r requirements.txt
```

## Ejecutar el servidor

Dentro de la carpeta `modulo3_api`, ejecuta:

```bash
uvicorn main:app --reload
```

La API queda disponible en:

```text
http://localhost:8000
```

La documentacion interactiva de Swagger esta en:

```text
http://localhost:8000/docs
```

## Autenticacion

La API usa JWT. Para consumir las rutas protegidas primero debes iniciar sesion en `/auth/login`.

Credenciales de prueba:

```text
username: admin
password: 1234
```

Importante: el login usa el flujo OAuth2 con formulario, no JSON. Por eso el `Content-Type` debe ser `application/x-www-form-urlencoded`.

Ejemplo con `curl`:

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=1234"
```

La respuesta devuelve un token con esta estructura:

```json
{
  "access_token": "TOKEN_GENERADO",
  "token_type": "bearer"
}
```

Para usar las rutas protegidas, envia el token en el header `Authorization`:

```text
Authorization: Bearer TOKEN_GENERADO
```

En Swagger puedes usar el boton **Authorize** y colocar:

```text
username: admin
password: 1234
client_id: dejar vacio
client_secret: dejar vacio
```

## Endpoints principales

### Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=1234"
```

### Listar tareas

```bash
curl http://localhost:8000/tasks \
  -H "Authorization: Bearer TOKEN_GENERADO"
```

### Crear tarea

```bash
curl -X POST http://localhost:8000/tasks \
  -H "Authorization: Bearer TOKEN_GENERADO" \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Mi tarea", "descripcion": "Descripcion de prueba", "estado": "pendiente"}'
```

Estados permitidos:

```text
pendiente
en_progreso
completado
```

### Actualizar estado de una tarea

```bash
curl -X PATCH http://localhost:8000/tasks/1 \
  -H "Authorization: Bearer TOKEN_GENERADO" \
  -H "Content-Type: application/json" \
  -d '{"estado": "completado"}'
```

### Eliminar tarea

```bash
curl -X DELETE http://localhost:8000/tasks/1 \
  -H "Authorization: Bearer TOKEN_GENERADO"
```

## Pruebas automaticas

El proyecto incluye pruebas con `pytest` para validar:

- Login exitoso
- Creacion de tarea con token valido
- Rechazo de acceso cuando no se envia token

Si estas dentro de `modulo3_api`, ejecuta:

```bash
pytest test/ -v
```

Si estas en la raiz del repositorio, ejecuta:

```bash
pytest modulo3_api/test -v
```

El archivo `pytest.ini` configura el path del proyecto para que los imports funcionen correctamente durante las pruebas.

## Estructura general

```text
modulo3_api/
+-- auth.py
+-- database.py
+-- main.py
+-- models.py
+-- pytest.ini
+-- requirements.txt
`-- test/
    `-- test_api.py
```

## Notas

- La base de datos usada en este proyecto es en memoria, por lo que las tareas se pierden al reiniciar el servidor.
- La clave JWT esta definida en `auth.py` solo para fines de prueba. En produccion deberia manejarse con variables de entorno.
- Las rutas de tareas requieren token Bearer, excepto `/auth/login`.
