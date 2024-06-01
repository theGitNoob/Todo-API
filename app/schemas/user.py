from pydantic import BaseModel

from app.schemas.todo_item import Item


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    model_config = {"from_attributes": True}
