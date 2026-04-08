from sqlmodel import SQLModel


class UsuarioCreate(SQLModel):
  username: str
  password: str


class UsuarioRead(SQLModel):
  id: str
  username: str


class UsuarioUpdate(SQLModel):
  username: str | None = None
  password: str | None = None
