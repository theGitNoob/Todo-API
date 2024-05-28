from datetime import datetime
from enum import Enum

from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel


class ItemStatus(str, Enum):
    pending = "pending"
    done = "done"
    in_progress = "in_progress"


class TodoItem(BaseModel):
    name: str
    description: str | None = None
    status: ItemStatus
    due_date: datetime | None = None


class TodoItemDto(BaseModel):
    id: int
    name: str
    description: str | None = None
    status: ItemStatus
    due_date: datetime | None = None


todo_items: dict = {
    1: TodoItem(
        name="Task 1",
        description="Task 1 description",
        status=ItemStatus.pending,
        due_date=datetime.now(),
    ),
    2: TodoItem(
        name="Task 2",
        description="Task 2 description",
        status=ItemStatus.done,
        due_date=datetime.now(),
    ),
    3: TodoItem(
        name="Task 3",
        description="Task 3 description",
        status=ItemStatus.in_progress,
        due_date=datetime.now(),
    ),
    4: TodoItem(
        name="Task 4",
        description="Task 4 description",
        status=ItemStatus.pending,
        due_date=datetime.now(),
    ),
}

app = FastAPI()


@app.get("/items")
async def get_all_items(
    item_status: ItemStatus | None = None, due_date: datetime | None = None
) -> list[TodoItemDto]:
    if len(todo_items) == 0:
        return []
    if item_status and due_date:
        return [
            TodoItemDto(id=item_id, **item.dict())
            for item_id, item in todo_items.items()
            if item.status == item_status and item.due_date == due_date
        ]
    elif item_status:
        return [
            TodoItemDto(id=item_id, **item.dict())
            for item_id, item in todo_items.items()
            if item.status == item_status
        ]
    if due_date:
        return [
            TodoItemDto(id=item_id, **item.dict())
            for item_id, item in todo_items.items()
            if item.due_date == due_date
        ]
    return [
        TodoItemDto(id=item_id, **item.dict()) for item_id, item in todo_items.items()
    ]


@app.get("/items/{item_id}")
async def get_item(item_id: int) -> TodoItem:
    todo_item = todo_items.get(item_id)
    if todo_item is None:
        raise HTTPException(
            status_code=404, detail=f"Item with id {item_id} was not found"
        )
    return todo_item


@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(item: TodoItem) -> TodoItemDto:
    item_id = len(todo_items)
    todo_items[item_id] = item
    return TodoItemDto(id=item_id, **item.dict())


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: TodoItem) -> TodoItemDto:
    _ = await get_item(item_id)
    todo_items[item_id] = item
    return TodoItemDto(id=item_id, **item.dict())


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    _ = await get_item(item_id)
    del todo_items[item_id]
