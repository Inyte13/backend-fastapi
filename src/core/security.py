import asyncio

import bcrypt

from src.core.config import settings


# encode: lo convierte a bytes
# decode: lo convierte a str
def hashear(password: str) -> str:
  return bcrypt.hashpw(
    password.encode(), bcrypt.gensalt(rounds=settings.salt_rounds)
  ).decode()


async def hashear_async(password: str) -> str:
  # Para que no se quede bloqueando el event loop
  return await asyncio.to_thread(hashear, password)


