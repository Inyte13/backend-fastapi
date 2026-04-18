import asyncio
from datetime import datetime, timedelta, timezone

import bcrypt
from fastapi import Cookie, HTTPException, Response
from jose import JWTError, jwt
from starlette import status

from src.core.database import SessionDep
from src.core.settings import settings
from src.crud.usuario import read_usuario
from src.models.refresh_token import RefreshToken
from src.models.usuario import Usuario


# encode: lo convierte a bytes
# decode: lo convierte a str
def hashear(password: str) -> str:
  return bcrypt.hashpw(
    password.encode(), bcrypt.gensalt(rounds=settings.salt_rounds)
  ).decode()


async def hashear_async(password: str) -> str:
  # Para que no se quede bloqueando el event loop
  return await asyncio.to_thread(hashear, password)


def verificar(password: str, hashed: str) -> bool:
  return bcrypt.checkpw(password.encode(), hashed.encode())


async def verificar_async(password: str, hashed: str) -> bool:
  return await asyncio.to_thread(verificar, password, hashed)


def crear_access_token(data: dict) -> str:
  payload = data.copy()
  payload['exp'] = datetime.now(timezone.utc) + timedelta(
    minutes=settings.access_token_duration_minutes
  )
  # Crea directamente todo el token, no solo la signature
  return jwt.encode(payload, settings.jwt_secret, algorithm='HS256')


def get_usuario(
  session: SessionDep, access_token: str | None = Cookie(default=None)
) -> Usuario:
  if not access_token:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

  try:
    payload = jwt.decode(
      access_token, settings.jwt_secret, algorithms=['HS256']
    )
    id = payload.get('id')

    if not id:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

  except JWTError:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

  usuario = read_usuario(session, id)
  if not usuario:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
  return usuario


def set_auth_cookies(
  response: Response, access_token: str, refresh_token: RefreshToken
):
  response.set_cookie(
    key='access_token',
    value=access_token,
    httponly=True,
    secure=settings.production,
    max_age=settings.access_token_duration_minutes * 60,
    samesite='strict',  # Solo se puede acceder en el mismo dominio
  )
  response.set_cookie(
    key='id_refresh_token',
    value=refresh_token.id,
    max_age=settings.refresh_token_duration_days * 86400,
    samesite='strict',  # Solo se puede acceder en el mismo dominio
  )
