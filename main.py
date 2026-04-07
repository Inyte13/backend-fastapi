from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.core.config import settings
from src.core.database import crear_tablas_y_db
from src.routers.auth import auth_router
from src.routers.usuario import usuario_router






if __name__ == '__main__':
  import uvicorn

  uvicorn.run('main:app', reload=True, port=settings.port)
