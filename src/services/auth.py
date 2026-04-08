from sqlmodel import Session

from src.core.security import hashear_async
from src.crud.usuario import create_usuario
from src.models.usuario import Usuario
from src.schemas.usuario import UsuarioCreate


async def registrar_usuario(
  session: Session, usuario: UsuarioCreate
) -> Usuario:
  pwd_hashed = await hashear_async(usuario.password)
  new_usuario = Usuario(username=usuario.username, password=pwd_hashed)
  return create_usuario(session, new_usuario)
