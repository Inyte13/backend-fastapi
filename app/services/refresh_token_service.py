import uuid
from datetime import datetime, timezone

from app.models.refresh_token import RefreshToken
from app.repositories.refresh_token_repository import (
  RefreshTokenCreate,
  refresh_token_repository,
)
from sqlalchemy.ext.asyncio import AsyncSession


class RefreshTokenService:
  def __init__(self):
    self.repository = refresh_token_repository

  async def crear_refresh_token(
    self, db: AsyncSession, id_usuario: uuid.UUID
  ) -> RefreshToken:
    refresh_token = RefreshTokenCreate(id_usuario=id_usuario)
    return await self.repository.create(db, refresh_token)

  async def buscar_refresh_token(
    self, db: AsyncSession, id: str
  ) -> RefreshToken:
    try:
      id_uuid = uuid.UUID(id)
    except ValueError:
      raise ValueError('ID de refresh token inválido')
    refresh_token = await self.repository.read(db, id_uuid)
    if not refresh_token:
      raise ValueError('Refresh Token no encontrado')

    expires_at = refresh_token.expires_at

    # Si no tiene UTC, le inyectamos
    if expires_at.tzinfo is None:
      expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at < datetime.now(timezone.utc):
      raise ValueError('Refresh Token expirado')

    return refresh_token

  async def eliminar_refresh_token(self, db: AsyncSession, id: str) -> None:
    try:
      id_uuid = uuid.UUID(id)
    except ValueError:
      raise ValueError('ID de refresh token inválido')
    await self.repository.delete(db, id_uuid)


refresh_token_service = RefreshTokenService()
