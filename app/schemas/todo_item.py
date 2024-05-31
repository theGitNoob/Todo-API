from datetime import datetime

from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    description: str | None = None
    status: str
    due_date: datetime | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
