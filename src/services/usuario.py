from sqlmodel import Session

from src.crud.usuario import (
  delete_usuario,
  read_usuario,
  update_usuario,
)
from src.models.usuario import Usuario
from src.schemas.usuario import UsuarioUpdate


def buscar_usuario(session: Session, id: str) -> Usuario:
  usuario = read_usuario(session, id)
  if not usuario:
    raise ValueError('Usuario no encontrado')
  return usuario


def actualizar_usuario(
  session: Session, id: str, usuario: UsuarioUpdate
) -> Usuario:
  usuario_bd = buscar_usuario(session, id)
  return update_usuario(session, usuario_bd, usuario)


def eliminar_usuario(session: Session, id: str) -> None:
  usuario = buscar_usuario(session, id)
  delete_usuario(session, usuario)
