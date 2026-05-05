import uuid
from typing import Generic, Sequence, TypeVar
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
Modelo = TypeVar('Modelo')
ModeloCreate = TypeVar('ModeloCreate', bound=BaseModel)
ModeloUpdate = TypeVar('ModeloUpdate', bound=BaseModel)
# En los params tenemos:
# Modelo SQLAlchemy
# Schemas Pydantic
class BaseRepository(Generic[Modelo, ModeloCreate, ModeloUpdate]):
  """Base repository para el CRUD de nuetros repositories"""

  def __init__(self, model: type[Modelo]):
    self.model = model

  async def create(self, db: AsyncSession, obj_in: ModeloCreate) -> Modelo:
    db_obj = self.model(**obj_in.model_dump())
    db.add(db_obj)
    await db.flush()
    await db.refresh(db_obj)
    return db_obj

  async def read(self, db: AsyncSession, id: uuid.UUID) -> Modelo | None:
    return await db.get(self.model, id)

  async def read_multi(
    self, db: AsyncSession, skip: int = 0, limit: int = 100
  ) -> Sequence[Modelo]:
    statement = select(self.model).offset(skip).limit(limit)
    result = await db.execute(statement)
    return result.scalars().all()

  async def update(
    self, db: AsyncSession, db_obj: Modelo, obj_in: ModeloUpdate
  ) -> Modelo:
    update_data = obj_in.model_dump(exclude_unset=True)
    # Parseamos de dict directamente actualizar los campos
    for field, value in update_data.items():
      setattr(db_obj, field, value)
    await db.flush()
    await db.refresh(db_obj)
    return db_obj

  async def delete(self, db: AsyncSession, id: uuid.UUID) -> bool:
    obj = await self.read(db, id)
    if obj:
      await db.delete(obj)
      return True
    return False
