from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from starlette import status
from src.core.database import SessionDep
from src.crud.usuario import read_usuarios
from src.schemas.usuario import UsuarioRead, UsuarioUpdate
