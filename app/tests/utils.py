from app.schemas.todo_item import ItemCreate
from app.schemas.user import UserCreate, User


def create_user(username: str, password: str, test_client) -> User:
    response = test_client.post(
        "/signup",
        json=UserCreate(username=username, password=password).model_dump(),
    )
    return response.json()


def login(username: str, password: str, test_client) -> str:
    _ = create_user(username, password, test_client)
    response = test_client.post(
        "/token",
        data={"username": username, "password": password},
    )
    return response.json()["access_token"]


def create_todo_item(item_in: ItemCreate, username: str, password: str, test_client):
    token = login(username, password, test_client)
    response = test_client.post(
        "/items/",
        json=item_in.model_dump(),
        headers={"Authorization": f"Bearer {token}"},
    )
    return response.json()
