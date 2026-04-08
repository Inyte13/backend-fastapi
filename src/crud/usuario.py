from typing import Sequence

from sqlmodel import Session, col, select

from src.models.usuario import Usuario
from src.schemas.usuario import UsuarioUpdate


def create_usuario(session: Session, usuario: Usuario) -> Usuario:
  session.add(usuario)
  session.commit()
  session.refresh(usuario)
  return usuario


def read_usuario(session: Session, id: str) -> Usuario | None:
  return session.get(Usuario, id)


def read_usuarios(session: Session) -> Sequence[Usuario]:
  statement = select(Usuario).order_by(col(Usuario.id))
  return session.exec(statement).all()


def update_usuario(
  session: Session, usuario_bd: Usuario, usuario: UsuarioUpdate
) -> Usuario:
  # model_dump === dict
  # Actualizamos solo los datos que envio con 'exclude_unset=True'
  usuario_bd.sqlmodel_update(usuario.model_dump(exclude_unset=True))
  session.add(usuario_bd)
  session.commit()
  session.refresh(usuario_bd)
  return usuario_bd


def delete_usuario(session: Session, usuario: Usuario):
  session.delete(usuario)
  session.commit()
