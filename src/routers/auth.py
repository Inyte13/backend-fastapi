from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from starlette import status

from src.core.database import SessionDep
from src.schemas.usuario import UsuarioCreate, UsuarioRead
from src.services.auth import registrar_usuario

auth_router = APIRouter(tags=['Auth'], prefix='/auth')


@auth_router.post('/login', status_code=201, response_model=UsuarioRead)
async def login(session: SessionDep, usuario: UsuarioCreate):
  try:
    return await registrar_usuario(session, usuario)
  except IntegrityError:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST, detail='El username ya existe'
    )
