import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel


class RefreshToken(SQLModel, table=True):
  id: str = Field(primary_key=True, default_factory=lambda: str(uuid.uuid4()))
  id_usuario: str = Field(foreign_key='usuario.id')
  expires_at: datetime
