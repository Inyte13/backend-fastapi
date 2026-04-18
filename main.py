from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from src.core.settings import settings
from src.core.database import crear_tablas_y_db
from src.core.auth import get_usuario
from src.routers.auth import auth_router
from src.routers.usuario import usuario_router

# Context manager de la app
@asynccontextmanager
async def lifespan(app: FastAPI):
  # Si no existen las tablas, las crea
  crear_tablas_y_db()
  yield  # Está corriendo
  # Al apagar puede ejecutar código como (cleanup, cerrar conexiones)


# Instancia principal de FastAPI con lifespan
app = FastAPI(
  lifespan=lifespan, title='OAuth App', version='1.0.0', openapi_version='3.0.0'
)

app.include_router(usuario_router, dependencies=[Depends(get_usuario)])
app.include_router(auth_router)

if __name__ == '__main__':
  import uvicorn

  uvicorn.run('main:app', reload=True, port=settings.port)
