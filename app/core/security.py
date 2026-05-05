import asyncio
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
from app.core.config import settings
from fastapi import Response
from jose import jwt


# encode: lo convierte a bytes
# decode: lo convierte a str
def hashear(password: str) -> str:
  return bcrypt.hashpw(
    password.encode(), bcrypt.gensalt(rounds=settings.SALT_ROUNDS)
  ).decode()


async def hashear_async(password: str) -> str:
  return await asyncio.to_thread(hashear, password)


def verificar(password: str, hashed: str) -> bool:
  return bcrypt.checkpw(password.encode(), hashed.encode())


async def verificar_async(password: str, hashed: str) -> bool:
  return await asyncio.to_thread(verificar, password, hashed)


# Any, para que pueda ser datetime
def crear_access_token(data: dict[str, Any]) -> str:
  payload = data.copy()
  payload['exp'] = datetime.now(timezone.utc) + timedelta(
    minutes=settings.ACCESS_TOKEN_DURATION_MINUTES
  )
  return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


def set_auth_cookies(
  response: Response, access_token: str, id_refresh_token: uuid.UUID
):
  response.set_cookie(
    key='access_token',
    value=access_token,
    httponly=True,
    secure=settings.PRODUCTION,
    max_age=settings.ACCESS_TOKEN_DURATION_MINUTES * 60,
    samesite='strict',  # Solo se puede acceder en el mismo dominio
  )
  response.set_cookie(
    key='id_refresh_token',
    value=str(id_refresh_token),
    max_age=settings.REFRESH_TOKEN_DURATION_DAYS * 86400,
    samesite='strict',  # Solo se puede acceder en el mismo dominio
  )
