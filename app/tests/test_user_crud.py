from app.schemas.todo_item import ItemCreate
from app.schemas.user import UserCreate


def test_create_user(test_client):
    response = test_client.post(
        "/signup",
        json=UserCreate(username="test1", password="test123").model_dump(),
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "test1"
    assert "id" in data
    assert "is_active" in data
    assert "items" in data


def test_read_users_items(test_client):
    response = test_client.post(
        "/signup", json=UserCreate(username="test2", password="test123").model_dump()
    )

    assert response.status_code == 200


def test_login(test_client):
    _ = test_client.post(
        "/signup",
        json=UserCreate(username="test1", password="test123").model_dump(),
    )
    response = test_client.post(
        "/token",
        data={"username": "test1", "password": "test123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_read_users_me(test_client):
    _ = test_client.post(
        "/signup", json=UserCreate(username="test1", password="test123").model_dump()
    )
    response = test_client.post(
        "/token",
        data={"username": "test1", "password": "test123"},
    )
    data = response.json()
    response = test_client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {data['access_token']}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "test1"
    assert "id" in data
    assert "is_active" in data
    assert "items" in data
    assert "hashed_password" not in data
    assert "password" not in data


def test_read_items(test_client):
    _ = test_client.post(
        "/signup", json=UserCreate(username="test1", password="test123").model_dump()
    )
    response = test_client.post(
        "/token",
        data={"username": "test1", "password": "test123"},
    )

    token = response.json()["access_token"]

    _ = test_client.post(
        "/items",
        json=ItemCreate(
            name="Item1", status="todo", description="This is item1"
        ).model_dump(),
        headers={"Authorization": f"Bearer {token}"},
    )

    _ = test_client.post(
        "/items",
        json=ItemCreate(
            name="Item2",
            status="pending",
            description="This is item2",
            due_date="2021-08-01T12:48:13",
        ).model_dump(),
        headers={"Authorization": f"Bearer {token}"},
    )

    response = test_client.get(
        "/users/me/items",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    assert data[0]["name"] == "Item1"
    assert data[0]["status"] == "todo"
    assert data[0]["description"] == "This is item1"
    assert data[0]["due_date"] is None
    # ------------------------------#
    assert data[1]["name"] == "Item2"
    assert data[1]["status"] == "pending"
    assert data[1]["description"] == "This is item2"
    assert data[1]["due_date"] == "2021-08-01T12:48:13"
