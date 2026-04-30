import uuid
from app.models.usuario import Usuario
from app.repositories.usuario_repository import usuario_repository
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from sqlalchemy.ext.asyncio import AsyncSession
