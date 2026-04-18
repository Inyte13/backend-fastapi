from datetime import datetime, timezone

from sqlmodel import Session

from src.crud.refresh_token import (
  create_refresh_token,
  delete_refresh_token,
  read_refresh_token,
  read_refresh_token_by_usuario,
)
from src.models.refresh_token import RefreshToken


def crear_refresh_token(session: Session, id_usuario: str) -> RefreshToken:
  refresh_token = read_refresh_token_by_usuario(session, id_usuario)
  if refresh_token:
    delete_refresh_token(session, refresh_token)
  new_refresh_token = create_refresh_token(session, id_usuario)
  return new_refresh_token


def buscar_refresh_token(session: Session, id: str) -> RefreshToken:
  refresh_token = read_refresh_token(session, id)
  if not refresh_token:
    raise ValueError('Refresh no encontrado')
  if refresh_token.expires_at < datetime.now(timezone.utc):
    raise ValueError('Refresh Token expirado')
  return refresh_token


def crear_refresh_token(session: Session, id_usuario: str) -> str:
  refresh_token = read_refresh_token_by_usuario(session, id_usuario)
  if refresh_token:
    delete_refresh_token(session, refresh_token)
  new_refresh_token = create_refresh_token(session, id_usuario)
  return new_refresh_token.id
