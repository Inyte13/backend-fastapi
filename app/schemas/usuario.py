import uuid

from pydantic import BaseModel, Field


class UsuarioCreate(BaseModel):
  username: str = Field(min_length=3, max_length=30)
  password: str = Field(min_length=6)


class UsuarioRead(BaseModel):
  id: uuid.UUID
  username: str
  # Solo va en Read porque es lo que respondemos, mandamos al usuario
  model_config = {'from_attributes': True}


class UsuarioUpdate(BaseModel):
  username: str | None = Field(default=None, min_length=3, max_length=30)
  password: str | None = Field(default=None, min_length=6)
