import uuid

from sqlmodel import Field, SQLModel


class Usuario(SQLModel, table=True):
  id: str = Field(
    default_factory=lambda: str(uuid.uuid4()), primary_key=True, nullable=False
  )
  username: str = Field(unique=True, min_length=3, nullable=False)
  password: str = Field(min_length=6, nullable=False)
