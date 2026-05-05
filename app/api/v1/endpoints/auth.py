from app.core.database import DbDep
from app.core.security import crear_access_token, set_auth_cookies
from app.schemas.usuario import UsuarioCreate, UsuarioRead
from app.services.auth_service import auth_service
from app.services.refresh_token_service import refresh_token_service
from fastapi import APIRouter, Cookie, HTTPException, Response, status

router = APIRouter(tags=['Auth'], prefix='/auth')


@router.post(
  '/register', status_code=status.HTTP_201_CREATED, response_model=UsuarioRead
)
async def register(db: DbDep, usuario: UsuarioCreate):
  try:
    return await auth_service.registrar_usuario(db, usuario)
  except ValueError as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
  '/login', status_code=status.HTTP_200_OK, response_model=UsuarioRead
)
# Declaramos explicitamente response para setear la cookie
async def login(db: DbDep, usuario: UsuarioCreate, response: Response):
  try:
    usuario_bd = await auth_service.loguear_usuario(db, usuario)
    access_token = crear_access_token({'id': str(usuario_bd.id)})
    refresh_token = await refresh_token_service.crear_refresh_token(
      db, usuario_bd.id
    )
    set_auth_cookies(response, access_token, refresh_token.id)
    return usuario_bd
  except ValueError as e:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post('/refresh')
async def refresh(
  db: DbDep,
  response: Response,
  id_refresh_token: str | None = Cookie(default=None),
):
  if not id_refresh_token:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
  try:
    refresh_token = await refresh_token_service.buscar_refresh_token(
      db, id_refresh_token
    )
    new_access_token = crear_access_token({'id': str(refresh_token.id_usuario)})
    new_refresh_token = await refresh_token_service.crear_refresh_token(
      db, refresh_token.id_usuario
    )
    await refresh_token_service.eliminar_refresh_token(db, id_refresh_token)
    set_auth_cookies(response, new_access_token, new_refresh_token.id)
  except (ValueError, AttributeError) as e:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post('/logout')
async def logout(
  db: DbDep,
  response: Response,
  id_refresh_token: str | None = Cookie(default=None),
):
  response.delete_cookie('access_token')
  response.delete_cookie('id_refresh_token')
  if id_refresh_token:
    await refresh_token_service.eliminar_refresh_token(db, id_refresh_token)
