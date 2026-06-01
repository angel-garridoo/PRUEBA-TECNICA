# Ejemplos de respuestas - Porthos Steakhouse & Pub

Estos ejemplos sirven para probar el endpoint `POST /responder` del modulo de IA.

El codigo actual usa Groq como proveedor y este modelo:

```text
meta-llama/llama-4-scout-17b-16e-instruct
```

Antes de ejecutar la API, revisa que tu archivo `.env` tenga la variable:

```text
GROQ_API_KEY=tu_api_key_de_groq
```

## Ejecutar el servidor

Desde la carpeta `modulo2_ia`:

```bash
uvicorn main:app --reload
```

Swagger queda disponible en:

```text
http://localhost:8000/docs
```

## Formato del request

El endpoint recibe un JSON con `motivo` y `detalle`:

```json
{
  "motivo": "consulta",
  "detalle": "Mensaje del cliente"
}
```

La respuesta mantiene esta estructura:

```json
{
  "respuesta": "Respuesta generada por la IA",
  "motivo": "consulta"
}
```

## Caso 1: Queja

Request:

```json
{
  "motivo": "queja",
  "detalle": "Pedi mi hamburguesa termino medio y llego completamente seca, ademas el domicilio tardo mas de una hora."
}
```

Ejemplo con `curl`:

```bash
curl -X POST http://localhost:8000/responder \
  -H "Content-Type: application/json" \
  -d '{"motivo": "queja", "detalle": "Pedi mi hamburguesa termino medio y llego completamente seca, ademas el domicilio tardo mas de una hora."}'
```

Respuesta esperada:

```json
{
  "respuesta": "Sentimos mucho que tu experiencia no haya sido la esperada, especialmente por el punto de coccion de la hamburguesa y la demora en el domicilio. Queremos revisar lo ocurrido con nuestro equipo para darte una mejor atencion en tu proximo pedido o visita. Gracias por contarnoslo, #ExperienciaPorthos",
  "motivo": "queja"
}
```

## Caso 2: Consulta

Request:

```json
{
  "motivo": "consulta",
  "detalle": "Tienen disponibilidad para reservar una mesa para 8 personas el sabado en la noche en Barranquilla?"
}
```

Ejemplo con `curl`:

```bash
curl -X POST http://localhost:8000/responder \
  -H "Content-Type: application/json" \
  -d '{"motivo": "consulta", "detalle": "Tienen disponibilidad para reservar una mesa para 8 personas el sabado en la noche en Barranquilla?"}'
```

Respuesta esperada:

```json
{
  "respuesta": "Claro, podemos ayudarte con una reserva para Barranquilla; te recomendamos comunicarte directamente con nuestros canales oficiales para confirmar disponibilidad exacta. Asi el equipo valida sede, hora y numero de personas en tiempo real. Te esperamos para vivir la #ExperienciaPorthos",
  "motivo": "consulta"
}
```

## Caso 3: Felicitacion

Request:

```json
{
  "motivo": "felicitacion",
  "detalle": "Quiero felicitar a todo el equipo de la sede de la Cra 53, la atencion fue increible y la Porthos Burger es lo mejor que he comido en mi vida."
}
```

Ejemplo con `curl`:

```bash
curl -X POST http://localhost:8000/responder \
  -H "Content-Type: application/json" \
  -d '{"motivo": "felicitacion", "detalle": "Quiero felicitar a todo el equipo de la sede de la Cra 53, la atencion fue increible y la Porthos Burger es lo mejor que he comido en mi vida."}'
```

Respuesta esperada:

```json
{
  "respuesta": "Que alegria leer tu mensaje! Compartiremos tus palabras con el equipo de la Cra 53, porque comentarios asi nos motivan a seguir cuidando cada detalle del servicio y de nuestras hamburguesas. Gracias por vivir la #ExperienciaPorthos",
  "motivo": "felicitacion"
}
```

## Caso 4: Validacion de campos vacios

Si `motivo` llega vacio, la API responde con `422`:

```json
{
  "motivo": "",
  "detalle": "Quiero saber el horario."
}
```

Respuesta esperada:

```json
{
  "detail": "El campo 'motivo' no puede estar vacio"
}
```

Si `detalle` llega vacio, tambien responde con `422`:

```json
{
  "motivo": "consulta",
  "detalle": ""
}
```

Respuesta esperada:

```json
{
  "detail": "El campo 'detalle' no puede estar vacio"
}
```

## Notas

- Las respuestas exactas pueden variar porque son generadas por IA.
- El prompt le pide al modelo responder en espanol, con tono calido y profesional.
- La respuesta debe cerrar con `#ExperienciaPorthos`.
- Si falta `GROQ_API_KEY`, el endpoint responde con error `500`.
