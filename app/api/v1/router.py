from app.api.v1.endpoints import auth, usuarios
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(usuarios.router)
