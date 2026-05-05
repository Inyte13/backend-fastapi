from contextlib import asynccontextmanager
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import Base, engine
from fastapi import FastAPI
