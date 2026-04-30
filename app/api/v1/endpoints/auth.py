from app.core.database import DbDep
from app.core.security import crear_access_token, set_auth_cookies
from app.schemas.usuario import UsuarioCreate, UsuarioRead
from app.services.auth_service import auth_service
from app.services.refresh_token_service import refresh_token_service
from fastapi import APIRouter, Cookie, HTTPException, Response, status
