from datetime import datetime
from enum import Enum

from fastapi import FastAPI, status, Response
from pydantic import BaseModel


class ItemStatus(str, Enum):
    pending = "pending"
    done = "done"
    in_progress = "in_progress"


class TodoItem(BaseModel):
    name: str
    description: str | None = None
    status: ItemStatus
    DueDate: datetime | None = None


todo_items: dict = {}

app = FastAPI()


@app.get("/items")
async def get_all_items():
    if len(todo_items) == 0:
        return {"message": "No items found"}
    return todo_items


@app.get("/items/{item_id}")
async def get_item(item_id: int, response: Response):
    if todo_items.get(item_id) is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Item with id {item_id} was not found"

    return todo_items.get(item_id)


@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(todo: TodoItem):
    item_id = len(todo_items)
    todo_items[item_id] = todo


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: TodoItem, response: Response):
    if todo_items.get(item_id) is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Item with id {item_id} was not found"
    todo_items[item_id] = item


@app.delete("/items/{item_id}")
async def delete_item(item_id: int, response: Response):
    if todo_items.get(item_id) is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Item with id {item_id} was not found"
    del todo_items[item_id]
    return {"message": "Item deleted successfully"}
