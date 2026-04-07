from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from starlette import status

from src.core.database import SessionDep
from src.schemas.usuario import UsuarioCreate, UsuarioRead
from src.services.auth import registrar_usuario



