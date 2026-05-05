import uuid
from app.core.database import Base
from sqlalchemy import String, Uuid
from sqlalchemy.orm import Mapped, mapped_column
class Usuario(Base):
  __tablename__ = 'usuarios'
  id: Mapped[uuid.UUID] = mapped_column(
    Uuid, primary_key=True, default=uuid.uuid4
  )
  username: Mapped[str] = mapped_column(String(30), unique=True)
  password: Mapped[str]
