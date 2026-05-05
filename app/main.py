from contextlib import asynccontextmanager

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import Base, engine
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
  """Application lifespan events"""
  # Startup: crea las tablas si no existen
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)
  yield
  # Shutdown


app = FastAPI(
  title='Runtime App',
  version='1.0.0',
  lifespan=lifespan,
)


# Include routers
app.include_router(api_router, prefix='/api/v1')

if __name__ == '__main__':
  import uvicorn

  uvicorn.run('app.main:app', reload=True, port=settings.PORT)
