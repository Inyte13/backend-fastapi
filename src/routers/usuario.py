from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from starlette import status

from src.core.database import SessionDep
from src.crud.usuario import read_usuarios
from src.schemas.usuario import UsuarioRead, UsuarioUpdate
from src.services.usuario import actualizar_usuario, eliminar_usuario

usuario_router = APIRouter(tags=['Usuarios'], prefix='/usuarios')


@usuario_router.get('/', response_model=list[UsuarioRead])
def get_usuarios(session: SessionDep):
  return read_usuarios(session)


@usuario_router.patch('/{id}', response_model=UsuarioRead)
def patch_usuario(session: SessionDep, usuario: UsuarioUpdate, id: str):
  try:
    return actualizar_usuario(session, id, usuario)
  except ValueError as e:
    raise HTTPException(status_code=404, detail=str(e))
  except IntegrityError:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST, detail='El username ya existe'
    )


@usuario_router.delete('/{id}', status_code=204)
def delete_usuario(session: SessionDep, id: str):
  try:
    eliminar_usuario(session, id)
  except ValueError as e:
    raise HTTPException(status_code=404, detail=str(e))
