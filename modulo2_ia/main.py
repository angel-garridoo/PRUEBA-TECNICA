import os
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from groq import Groq, APITimeoutError, RateLimitError, AuthenticationError, BadRequestError
from dotenv import load_dotenv
from prompt import construir_prompt

# Carga variables desde el archivo .env ubicado en la raiz del proyecto.
load_dotenv()

app = FastAPI(
    title="Asistente de Atencion al Cliente - Porthos Steakhouse & Pub",
    description="Genera respuestas profesionales a mensajes de clientes usando IA",
    version="1.0.0"
)


class MensajeCliente(BaseModel):
    motivo: str
    detalle: str


class RespuestaAsistente(BaseModel):
    respuesta: str
    motivo: str


@app.post("/responder", response_model=RespuestaAsistente)
def responder_cliente(mensaje: MensajeCliente):

    # Validamos estos campos antes de llamar al modelo para evitar solicitudes incompletas.
    if not mensaje.motivo.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El campo 'motivo' no puede estar vacio"
        )
    if not mensaje.detalle.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El campo 'detalle' no puede estar vacio"
        )

    # La API key vive fuera del codigo para no exponer secretos en el repositorio.
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API key de Groq no configurada en el servidor"
        )

    # El prompt concentra la identidad de marca y las reglas de respuesta.
    prompt = construir_prompt(mensaje.motivo, mensaje.detalle)

    try:
        cliente = Groq(api_key=api_key)
        respuesta = cliente.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": f"Motivo: {mensaje.motivo}\nMensaje del cliente: {mensaje.detalle}"
                }
            ],
            # Limita respuestas largas y mantiene un tono natural sin volverlo impredecible.
            max_tokens=200,
            temperature=0.7,
        )

        texto_respuesta = respuesta.choices[0].message.content.strip()

        return RespuestaAsistente(
            respuesta=texto_respuesta,
            motivo=mensaje.motivo
        )

    # Los errores se traducen a HTTP para que el cliente reciba respuestas claras.
    except APITimeoutError:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="La API de Groq no respondio a tiempo. Intenta de nuevo."
        )

    except RateLimitError:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Limite de uso de la API alcanzado. Espera un momento."
        )

    except AuthenticationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key de Groq invalida. Verifica la configuracion."
        )

    except BadRequestError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El mensaje no pudo procesarse: {str(e)}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado: {str(e)}"
        )
