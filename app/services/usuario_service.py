import uuid

from app.models.usuario import Usuario
from app.repositories.usuario_repository import usuario_repository
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from sqlalchemy.ext.asyncio import AsyncSession


class UsuarioService:
  def __init__(self):
    self.repository = usuario_repository

  async def crear_usuario(
    self, db: AsyncSession, usuario: UsuarioCreate
  ) -> Usuario:
    existente = await self.repository.read_by_username(db, usuario.username)
    if existente:
      raise ValueError('El username ya existe')
    return await self.repository.create(db, obj_in=usuario)

  async def buscar_usuario(self, db: AsyncSession, id: uuid.UUID) -> Usuario:
    usuario = await self.repository.read(db, id)
    if not usuario:
      raise ValueError('Usuario no encontrado')
    return usuario

  async def buscar_by_username(
    self, db: AsyncSession, username: str
  ) -> Usuario:
    usuario = await self.repository.read_by_username(db, username)
    if not usuario:
      raise ValueError('Usuario no encontrado')
    return usuario

  async def actualizar_usuario(
    self, db: AsyncSession, id: uuid.UUID, usuario: UsuarioUpdate
  ) -> Usuario:
    usuario_bd = await self.buscar_usuario(db, id)
    if usuario.username and usuario.username != usuario_bd.username:
      if await self.repository.read_by_username(db, usuario.username):
        raise ValueError('El username ya existe')
    return await self.repository.update(db, db_obj=usuario_bd, obj_in=usuario)

  async def eliminar_usuario(self, db: AsyncSession, id: uuid.UUID) -> None:
    if not await self.repository.delete(db, id):
      raise ValueError('Usuario no encontrado')


usuario_service = UsuarioService()
