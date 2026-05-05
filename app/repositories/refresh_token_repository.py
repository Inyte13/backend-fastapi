import uuid
from datetime import datetime, timedelta, timezone
from typing import override

from app.core.config import settings
from app.models.refresh_token import RefreshToken
from app.repositories.base_repository import BaseRepository
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession


# Creamos este schema para incluirlo en el modelo y lo podamos usar para crear nosotros el refresh token
class RefreshTokenCreate(BaseModel):
  id_usuario: uuid.UUID


class RefreshTokenRepository(
  BaseRepository[
    RefreshToken,
    RefreshTokenCreate,
    BaseModel,  # BaseModel porque no tiene schemas
  ]
):
  @override
  async def create(
    self, db: AsyncSession, obj_in: RefreshTokenCreate
  ) -> RefreshToken:
    expires_at = datetime.now(timezone.utc) + timedelta(
      days=settings.REFRESH_TOKEN_DURATION_DAYS
    )
    db_obj = self.model(id_usuario=obj_in.id_usuario, expires_at=expires_at)
    db.add(db_obj)
    await db.flush()
    await db.refresh(db_obj)
    return db_obj


refresh_token_repository = RefreshTokenRepository(RefreshToken)
