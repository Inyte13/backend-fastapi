import uuid
from typing import Annotated
from app.core.config import settings
from app.core.database import get_db
from app.models.usuario import Usuario
from app.repositories.usuario_repository import usuario_repository
from fastapi import Cookie, Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
