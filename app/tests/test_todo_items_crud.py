from app.schemas.todo_item import ItemCreate

from app.tests.utils import login, create_todo_item


def test_create_todo_item(test_client):

    token = login("test1", "test123", test_client)
    item_in = ItemCreate(
        name="test item",
        description="test description",
        due_date="2022-12-01",
        status="todo",
    )
    response = test_client.post(
        "/items/",
        json=item_in.model_dump(),
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    item = response.json()
    assert item["name"] == "test item"
    assert item["description"] == "test description"
    assert item["due_date"] == "2022-12-01"
    assert item["status"] == "todo"
    assert "id" in item
    assert "owner_id" in item


def test_read_todo_item(test_client):

    item = create_todo_item(
        ItemCreate(
            name="test item",
            description="test description",
            due_date="2022-12-01",
            status="todo",
        ),
        "test1",
        "test123",
        test_client,
    )
    token = login("test1", "test123", test_client)
    response = test_client.get(
        f"/items/{item['id']}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    item = response.json()
    assert item["name"] == "test item"
    assert item["description"] == "test description"
    assert item["due_date"] == "2022-12-01"
    assert item["status"] == "todo"
    assert "id" in item
    assert "owner_id" in item


def test_read_all_todo_items(test_client):
    for i in range(3):
        create_todo_item(
            ItemCreate(
                name=f"test item {i}",
                description=f"test description {i}",
                due_date="2022-12-01",
                status="todo",
            ),
            "test1",
            "test123",
            test_client,
        )
    token = login("test1", "test123", test_client)
    response = test_client.get("/items/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 3
    for i, item in enumerate(items):
        assert item["name"] == f"test item {i}"
        assert item["description"] == f"test description {i}"
        assert item["due_date"] == "2022-12-01"
        assert item["status"] == "todo"
        assert "id" in item
        assert "owner_id" in item


def test_update_todo_item(test_client):
    item = create_todo_item(
        ItemCreate(
            name="test item",
            description="test description",
            due_date="2022-12-01",
            status="todo",
        ),
        "test1",
        "test123",
        test_client,
    )
    token = login("test1", "test123", test_client)
    response = test_client.put(
        f"/items/{item['id']}",
        json=ItemCreate(
            name="updated test item",
            description="updated test description",
            due_date="2022-12-01",
            status="done",
        ).model_dump(),
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    updated_item = response.json()
    assert updated_item["name"] == "updated test item"
    assert updated_item["description"] == "updated test description"
    assert updated_item["due_date"] == "2022-12-01"
    assert updated_item["status"] == "done"
    assert "id" in updated_item
    assert "owner_id" in updated_item


def test_delete_todo_item(test_client):
    item = create_todo_item(
        ItemCreate(
            name="test item",
            description="test description",
            due_date="2022-12-01",
            status="todo",
        ),
        "test1",
        "test123",
        test_client,
    )
    token = login("test1", "test123", test_client)
    response = test_client.delete(
        f"/items/{item['id']}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204
    response = test_client.get(
        f"/items/{item['id']}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
