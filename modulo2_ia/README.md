# Modulo 2 - Asistente IA para atencion al cliente

Este modulo expone una API con FastAPI que genera respuestas automaticas para mensajes de clientes de Porthos Steakhouse & Pub.

La idea es recibir un motivo y un detalle del mensaje, construir un prompt con el contexto de la marca y enviar ese prompt a un modelo de IA usando Groq. La API devuelve una respuesta breve, en espanol, con tono calido y profesional.

## Que hace este modulo

- Recibe mensajes de clientes mediante `POST /responder`.
- Valida que los campos requeridos no lleguen vacios.
- Construye un prompt con contexto de Porthos desde `prompt.py`.
- Llama a Groq usando el modelo configurado en `main.py`.
- Devuelve una respuesta lista para usar en atencion al cliente.
- Maneja errores comunes como falta de API key, timeouts, limites de uso y mensajes invalidos.

## Stack tecnico

- Python 3.11+
- FastAPI
- Uvicorn
- Groq SDK
- python-dotenv
- Pydantic

Modelo usado actualmente:

```text
meta-llama/llama-4-scout-17b-16e-instruct
```

## Estructura del modulo

```text
modulo2_ia/
+-- main.py
+-- prompt.py
+-- requirements.txt
+-- README.md
`-- ejemplos.md
```

## Configuracion de variables de entorno

Este modulo necesita una API key de Groq. Debe estar definida en el archivo `.env` ubicado en la raiz del proyecto:

```env
GROQ_API_KEY=tu_api_key_de_groq
```

El archivo `.env` no debe subirse al repositorio porque contiene credenciales privadas. Para eso, la raiz del proyecto debe tener un `.gitignore` que ignore `.env`.

## Instalacion

Desde la raiz del repositorio:

```bash
cd modulo2_ia
pip install -r requirements.txt
```

## Ejecutar el servidor

Dentro de `modulo2_ia`, ejecuta:

```bash
uvicorn main:app --reload
```

La API quedara disponible en:

```text
http://localhost:8000
```

La documentacion interactiva de Swagger queda en:

```text
http://localhost:8000/docs
```

## Endpoint principal

### `POST /responder`

Genera una respuesta para un mensaje de cliente.

Request:

```json
{
  "motivo": "consulta",
  "detalle": "Quiero saber si tienen reservas para el sabado en la noche."
}
```

Response:

```json
{
  "respuesta": "Respuesta generada por la IA",
  "motivo": "consulta"
}
```

## Validaciones

La API valida que `motivo` y `detalle` no lleguen vacios.

Si `motivo` esta vacio, responde con `422`:

```json
{
  "detail": "El campo 'motivo' no puede estar vacio"
}
```

Si `detalle` esta vacio, responde con `422`:

```json
{
  "detail": "El campo 'detalle' no puede estar vacio"
}
```

## Manejo de errores

El endpoint captura errores comunes y responde con codigos HTTP claros:

- `500`: falta `GROQ_API_KEY` o hubo un error inesperado.
- `504`: la API de Groq no respondio a tiempo.
- `429`: se alcanzo un limite de uso o rate limit.
- `401`: la API key de Groq no es valida.
- `400`: el mensaje no pudo procesarse por un error de solicitud.

## Ejemplo rapido con curl

```bash
curl -X POST http://localhost:8000/responder \
  -H "Content-Type: application/json" \
  -d '{"motivo": "queja", "detalle": "Pedi mi hamburguesa termino medio y llego seca, ademas el domicilio tardo mas de una hora."}'
```

Respuesta esperada:

```json
{
  "respuesta": "Sentimos mucho que tu experiencia no haya sido la esperada. Queremos revisar lo ocurrido con nuestro equipo para darte una mejor atencion en tu proximo pedido o visita. Gracias por contarnoslo, #ExperienciaPorthos",
  "motivo": "queja"
}
```

Las respuestas pueden variar porque son generadas por IA, pero deben respetar las reglas definidas en `prompt.py`.

## Prompt del asistente

El archivo `prompt.py` define la personalidad y las reglas del asistente. Incluye:

- Contexto de Porthos Steakhouse & Pub.
- Datos clave del negocio.
- Tono de respuesta.
- Restricciones para no inventar precios, reservas o compensaciones.
- Regla de cerrar con `#ExperienciaPorthos`.

El prompt busca que las respuestas sean utiles, breves y consistentes con la marca.

## Mas ejemplos

Puedes ver mas casos de uso en:

```text
ejemplos.md
```

Ese archivo incluye ejemplos para quejas, consultas, felicitaciones y validaciones de campos vacios.

## Notas importantes

- El servidor debe ejecutarse desde la carpeta `modulo2_ia`.
- La API key se lee con `load_dotenv()`, por eso el `.env` debe existir antes de probar el endpoint.
- Si cambias el proveedor o el modelo de IA, actualiza tambien `requirements.txt`, `main.py`, `README.md` y `ejemplos.md`.
