from datetime import datetime

from sqlalchemy.orm import Session

from app.models.todo_item import Item, ItemStatus
from app.schemas.todo_item import ItemCreate


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Item).offset(skip).limit(limit).all()


def filter_items(
    db: Session,
    item_status: ItemStatus | None = None,
    due_date: datetime | None = None,
) -> list[Item]:
    items = db.query(Item).all()
    if item_status:
        items = list(filter(lambda x: x.status == item_status, items))
    if due_date:
        items = list(filter(lambda x: x.due_date == due_date, items))
    return items


def create_user_item(db: Session, item: ItemCreate, user_id: int):
    db_item = Item(**item.model_dump(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(db: Session, item_id: int, item: ItemCreate):
    db_item = get_item(db, item_id)
    db_item.name = item.name
    db_item.description = item.description
    db_item.status = item.status
    db_item.due_date = item.due_date
    db.commit()
    db.refresh(db_item)
    return db_item


def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()


def delete_item(db: Session, item_id: int):
    db_item = get_item(db, item_id)
    if db_item:
        db.delete(db_item)
        db.commit()
        return db_item
