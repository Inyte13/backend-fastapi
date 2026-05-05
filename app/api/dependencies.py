import uuid
from typing import Annotated

from app.core.config import settings
from app.core.database import get_db
from app.models.usuario import Usuario
from app.repositories.usuario_repository import usuario_repository
from fastapi import Cookie, Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession


async def get_usuario(
  db: AsyncSession = Depends(get_db),
  access_token: str | None = Cookie(default=None),
) -> Usuario:

  if not access_token:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

  try:
    payload = jwt.decode(
      access_token, settings.SECRET_KEY, algorithms=['HS256']
    )
    id_str = payload.get('id')

    if not id_str:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # Convertidmos el id_str a uuid para el read
    try:
      id_uuid = uuid.UUID(id_str)
    except ValueError:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

  except JWTError:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

  usuario = await usuario_repository.read(db, id_uuid)
  if not usuario:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

  return usuario


UsuarioActualDep = Annotated[Usuario, Depends(get_usuario)]
