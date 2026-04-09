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


