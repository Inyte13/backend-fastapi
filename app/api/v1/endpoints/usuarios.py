import uuid

from app.api.dependencies import UsuarioActualDep
from app.core.database import DbDep
from app.schemas.usuario import UsuarioRead, UsuarioUpdate
from app.services.auth_service import auth_service
from app.services.usuario_service import usuario_service
from fastapi import APIRouter, HTTPException, status

router = APIRouter(tags=['Usuarios'], prefix='/usuarios')


@router.get('/', response_model=list[UsuarioRead])
async def get_usuarios(db: DbDep):
  return await usuario_service.repository.read_multi(db)


@router.patch('/{id}', response_model=UsuarioRead)
async def patch_usuario(
  id: uuid.UUID,
  usuario: UsuarioUpdate,
  db: DbDep,
  usuario_actual: UsuarioActualDep,
):
  if usuario_actual.id != id:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail='No puedes editar otro usuario',
    )
  try:
    return await auth_service.actualizar_usuario(db, id, usuario)
  except ValueError as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(
  id: uuid.UUID,
  db: DbDep,
  usuario_actual: UsuarioActualDep,
):
  if usuario_actual.id != id:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail='No puedes eliminar otro usuario',
    )
  try:
    await usuario_service.eliminar_usuario(db, id)
  except ValueError as e:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
