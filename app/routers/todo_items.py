from datetime import datetime
from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.todo_item import ItemStatus
from app.models.user import User
from app.schemas.todo_item import Item, ItemCreate
from app.utils.auth import get_current_active_user
from app.utils.todo_item_utils import (
    create_user_item,
    update_item,
    delete_item,
    get_item,
    filter_items,
)

router = APIRouter(
    prefix="/items",
    tags=["Todo Items"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[Item])
async def get_all(
    status: ItemStatus | None = None,
    due_date: datetime | None = None,
    db: Session = Depends(get_db),
) -> list[Item]:
    return filter_items(db, status, due_date)


@router.get("/{item_id}", response_model=Item)
async def get(item_id: int, db: Session = Depends(get_db)):
    todo_item = get_item(db, item_id)
    if todo_item is None:
        raise HTTPException(status_code=404, detail=f"Item  not found")
    return todo_item


@router.post("/", response_model=Item, status_code=201)
async def create_item(
    item: ItemCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    return create_user_item(db, item, current_user.id)


@router.put("/{item_id}", response_model=Item)
async def update(item_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    return update_item(db, item_id, item)


@router.delete("/{item_id}", status_code=204)
async def delete(item_id: int, db: Session = Depends(get_db)):
    deleted_item = delete_item(db, item_id)
    if deleted_item is None:
        raise HTTPException(status_code=404, detail=f"Item not found")
