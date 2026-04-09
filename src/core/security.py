import asyncio
from datetime import datetime, timedelta, timezone

import bcrypt
from fastapi import Cookie, HTTPException
from jose import JWTError, jwt
from starlette import status

from src.core.database import SessionDep
from src.core.settings import settings
from src.crud.usuario import read_usuario
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
def crear_token(data: dict) -> str:
  payload = data.copy()
  payload['exp'] = datetime.now(timezone.utc) + timedelta(
    minutes=settings.access_token_duration_minutes
  )
  return jwt.encode(payload, settings.jwt_secret, algorithm='HS256')
