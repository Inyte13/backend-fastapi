from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel

DATABASE_URL = 'sqlite:///./auth.db'
engine = create_engine(
  DATABASE_URL, connect_args={'check_same_thread': False}, echo=False
)


# Crear nuestras tablas
def crear_tablas_y_db():
  SQLModel.metadata.create_all(engine)


# Crea y cierra la sesión automáticamente por cada request
def get_session():
  with Session(engine) as session:
    yield session


SessionDep = Annotated[Session, Depends(get_session)]


