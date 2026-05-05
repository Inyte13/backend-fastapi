from app.models.usuario import Usuario
from app.repositories.base_repository import BaseRepository
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class UsuarioRepository(BaseRepository[Usuario, UsuarioCreate, UsuarioUpdate]):
  async def read_by_username(
    self, db: AsyncSession, username: str
  ) -> Usuario | None:
    statement = select(Usuario).where(Usuario.username == username)
    result = await db.execute(statement)
    return result.scalars().first()


usuario_repository = UsuarioRepository(Usuario)
