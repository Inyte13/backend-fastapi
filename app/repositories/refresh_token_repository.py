import uuid
from datetime import datetime, timedelta, timezone
from typing import override
from app.core.config import settings
from app.models.refresh_token import RefreshToken
from app.repositories.base_repository import BaseRepository
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
