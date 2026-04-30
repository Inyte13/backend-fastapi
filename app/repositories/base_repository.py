import uuid
from typing import Generic, Sequence, TypeVar
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
