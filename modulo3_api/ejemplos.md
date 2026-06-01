# Ejemplos de uso

Este archivo muestra ejemplos practicos para probar la API desde Swagger, `curl` o PowerShell. La idea es seguir el flujo normal: iniciar sesion, copiar el token y usarlo en las rutas protegidas.

## 1. Iniciar el servidor

Desde la carpeta `modulo3_api`:

```bash
uvicorn main:app --reload
```

La documentacion interactiva queda disponible en:

```text
http://localhost:8000/docs
```

## 2. Login

Credenciales de prueba:

```text
username: admin
password: 1234
```

El login usa formulario OAuth2. Por eso se envia con `application/x-www-form-urlencoded`, no con JSON.

### Con curl

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=1234"
```

### Con PowerShell

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri "http://localhost:8000/auth/login" `
  -ContentType "application/x-www-form-urlencoded" `
  -Body "username=admin&password=1234"
```

Respuesta esperada:

```json
{
  "access_token": "TOKEN_GENERADO",
  "token_type": "bearer"
}
```

## 3. Autorizar en Swagger

En `http://localhost:8000/docs`, presiona **Authorize** y usa:

```text
username: admin
password: 1234
client_id: dejar vacio
client_secret: dejar vacio
```

Despues de autorizar, Swagger enviara automaticamente el token en las rutas protegidas.

## 4. Crear una tarea

Reemplaza `TOKEN_GENERADO` por el `access_token` que devolvio el login.

```bash
curl -X POST http://localhost:8000/tasks \
  -H "Authorization: Bearer TOKEN_GENERADO" \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Preparar entrega", "descripcion": "Revisar README, tests y ejemplos", "estado": "pendiente"}'
```

Respuesta esperada:

```json
{
  "id": 1,
  "titulo": "Preparar entrega",
  "descripcion": "Revisar README, tests y ejemplos",
  "estado": "pendiente"
}
```

## 5. Listar tareas

```bash
curl http://localhost:8000/tasks \
  -H "Authorization: Bearer TOKEN_GENERADO"
```

## 6. Actualizar una tarea

Estados permitidos:

```text
pendiente
en_progreso
completado
```

Ejemplo:

```bash
curl -X PATCH http://localhost:8000/tasks/1 \
  -H "Authorization: Bearer TOKEN_GENERADO" \
  -H "Content-Type: application/json" \
  -d '{"estado": "completado"}'
```

## 7. Eliminar una tarea

```bash
curl -X DELETE http://localhost:8000/tasks/1 \
  -H "Authorization: Bearer TOKEN_GENERADO"
```

Si la tarea existe, la API responde con estado `204 No Content`.

## 8. Probar el rechazo sin token

Esta peticion no envia `Authorization`, por eso debe responder `401 Unauthorized`.

```bash
curl http://localhost:8000/tasks
```

Este mismo caso esta cubierto por las pruebas automaticas en `test/test_api.py`.
