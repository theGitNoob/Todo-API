from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    description: str | None = None
    status: str
    due_date: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    model_config = {"from_attributes": True}
