import uuid

from app.core.security import hashear_async, verificar_async
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.services.usuario_service import usuario_service
from sqlalchemy.ext.asyncio import AsyncSession


class AuthService:
  def __init__(self):
    self.usuario_service = usuario_service

  async def registrar_usuario(
    self, db: AsyncSession, usuario: UsuarioCreate
  ) -> Usuario:
    pwd_hashed = await hashear_async(usuario.password)
    usuario_dict = usuario.model_dump()
    usuario_dict['password'] = pwd_hashed
    return await self.usuario_service.crear_usuario(
      db, usuario=UsuarioCreate(**usuario_dict)
    )

  async def loguear_usuario(
    self, db: AsyncSession, usuario: UsuarioCreate
  ) -> Usuario:
    usuario_bd = await self.usuario_service.buscar_by_username(
      db, usuario.username
    )
    if not await verificar_async(usuario.password, usuario_bd.password):
      raise ValueError('Credenciales incorrectas')
    return usuario_bd

  async def actualizar_usuario(
    self, db: AsyncSession, id: uuid.UUID, usuario: UsuarioUpdate
  ) -> Usuario:
    if usuario.password:
      usuario_dict = usuario.model_dump(exclude_unset=True)
      usuario_dict['password'] = await hashear_async(usuario.password)
      usuario = UsuarioUpdate(**usuario_dict)
    return await self.usuario_service.actualizar_usuario(db, id, usuario)


auth_service = AuthService()
