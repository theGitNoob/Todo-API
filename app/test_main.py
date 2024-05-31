from datetime import datetime

from fastapi import status
from fastapi.testclient import TestClient

from app.main import todo_items, ItemStatus, TodoItem, app

client = TestClient(app)


def test_get_all_items():
    response = client.get("/items")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == len(todo_items)


def test_get_all_items_filtered():
    response = client.get("/items?item_status=pending&due_date=2023-01-01")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1


def test_get_item():
    response = client.get("/items/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == todo_items[1].name


def test_get_item_not_found():
    response = client.get("/items/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_item():
    item = TodoItem(name="Task 5", status=ItemStatus.pending, due_date=datetime.now())
    item_dict = item.model_dump()
    item_dict["due_date"] = item_dict["due_date"].isoformat()
    response = client.post("/items/", json=item_dict)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == item.name


def test_update_item():
    item = TodoItem(
        name="Updated Task", status=ItemStatus.done, due_date=datetime.now()
    )
    item_dict = item.model_dump()
    item_dict["due_date"] = item_dict["due_date"].isoformat()
    response = client.put("/items/1", json=item_dict)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == item.name


def test_update_item_not_found():
    item = TodoItem(
        name="Updated Task", status=ItemStatus.done, due_date=datetime.now()
    )
    item_dict = item.model_dump()
    item_dict["due_date"] = item_dict["due_date"].isoformat()
    response = client.put("/items/999", json=item_dict)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_item():
    response = client.delete("/items/1")
    assert response.status_code == status.HTTP_200_OK


def test_delete_item_not_found():
    response = client.delete("/items/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
