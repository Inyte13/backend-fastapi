import asyncio
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any
import bcrypt
from app.core.config import settings
from fastapi import Response
from jose import jwt
