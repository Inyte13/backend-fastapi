from typing import Annotated
from app.core.config import settings
from fastapi import Depends
from sqlalchemy.ext.asyncio import (
  AsyncSession,
  async_sessionmaker,
  create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
