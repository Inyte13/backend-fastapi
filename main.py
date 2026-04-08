from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.core.config import settings
from src.core.database import crear_tablas_y_db
from src.routers.auth import auth_router
from src.routers.usuario import usuario_router

# Context manager de la app
@asynccontextmanager
async def lifespan(app: FastAPI):
  # Si no existen las tablas, las crea
  crear_tablas_y_db()
  yield  # Está corriendo
  # Al apagar puede ejecutar código como (cleanup, cerrar conexiones)




if __name__ == '__main__':
  import uvicorn

  uvicorn.run('main:app', reload=True, port=settings.port)
