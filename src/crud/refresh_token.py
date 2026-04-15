from datetime import datetime, timedelta, timezone

from sqlmodel import Session, select

from src.core.settings import settings
from src.models.refresh_token import RefreshToken


def create_refresh_token(session: Session, id_usuario: str) -> RefreshToken:
  expires_at = datetime.now(timezone.utc) + timedelta(
    days=settings.refresh_token_duration_days
  )
  refresh_token = RefreshToken(id_usuario=id_usuario, expires_at=expires_at)
  session.add(refresh_token)
  session.commit()
  session.refresh(refresh_token)
  return refresh_token


def read_refresh_token(session: Session, id: str) -> RefreshToken | None:
  return session.get(RefreshToken, id)


def read_refresh_token_by_usuario(
  session: Session, id_usuario: str
) -> RefreshToken | None:
  statement = select(RefreshToken).where(RefreshToken.id_usuario == id_usuario)
  return session.exec(statement).first()


def delete_refresh_token(session: Session, refresh_token: RefreshToken):
  session.delete(refresh_token)
  session.commit()
