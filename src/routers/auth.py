from fastapi import APIRouter, Cookie, HTTPException, Response
from sqlalchemy.exc import IntegrityError
from starlette import status

from src.core.auth import crear_access_token, set_auth_cookies
from src.core.database import SessionDep
from src.schemas.usuario import UsuarioCreate, UsuarioRead
from src.services.auth import loguear_usuario, registrar_usuario
from src.services.refresh_token import (
  buscar_refresh_token,
  crear_refresh_token,
  eliminar_refresh_token,
)

auth_router = APIRouter(tags=['Auth'], prefix='/auth')


@auth_router.post('/register', status_code=201, response_model=UsuarioRead)
async def register(session: SessionDep, usuario: UsuarioCreate):
  try:
    return await registrar_usuario(session, usuario)
  except IntegrityError:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST, detail='El username ya existe'
    )


# Declaramos explicitamente response para setear la cookie
@auth_router.post('/login', status_code=201, response_model=UsuarioRead)
async def login(
  session: SessionDep, usuario: UsuarioCreate, response: Response
):
  try:
    usuario_bd = await loguear_usuario(session, usuario)
    access_token = crear_access_token({'id': usuario_bd.id})
    refresh_token = crear_refresh_token(session, usuario_bd.id)
    set_auth_cookies(response, access_token, refresh_token)
    return usuario_bd
  except ValueError as e:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
