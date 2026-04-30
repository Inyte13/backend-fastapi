import uuid
from app.api.dependencies import UsuarioActualDep
from app.core.database import DbDep
from app.schemas.usuario import UsuarioRead, UsuarioUpdate
from app.services.auth_service import auth_service
from app.services.usuario_service import usuario_service
from fastapi import APIRouter, HTTPException, status
