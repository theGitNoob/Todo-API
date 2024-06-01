from fastapi import FastAPI

from .database import Base, engine
from .middlewares import body_logger
from .routers import users, todo_items

Base.metadata.create_all(bind=engine)


app = FastAPI()

app.middleware("http")(body_logger.log_request)
app.include_router(users.router)
app.include_router(todo_items.router)
