from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

# Clave usada para firmar los JWT. En produccion deberia venir de una variable de entorno.
SECRET_KEY = "clave-super-secreta-cambiar-en-produccion"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Usuario fijo para la prueba tecnica; en una app real vendria de una base de datos.
FAKE_USER = {
    "username": "admin",
    "password": "1234"
}

# FastAPI usa este esquema para leer el token Bearer en las rutas protegidas.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def verify_credentials(username: str, password: str) -> bool:

    return (
        username == FAKE_USER["username"] and
        password == FAKE_USER["password"]
    )


def create_access_token(username: str) -> str:

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # El campo "sub" identifica al usuario dentro del token.
    payload = {
        "sub": username,
        "exp": expire
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token: str = Depends(oauth2_scheme)) -> str:

    # Si el token falta, expiro o no se puede validar, la API responde 401.
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception
        return username
    except JWTError:

        raise credentials_exception
