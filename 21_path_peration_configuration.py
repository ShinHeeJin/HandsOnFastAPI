from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


# add tags to your path operation
@app.post("/items/", response_model=Item, tags=["items"])
async def create_item(item: Item):
    return item


@app.get("/items/", tags=["items"])
async def read_items():
    return [{"name": "Foo", "price": 42}]


@app.get("/users/", tags=["users"])
async def resd_users():
    return [{"username": "johndeo"}]


class Tags(Enum):
    items = "items"
    users = "users"


# Tags with Enums
@app.get("/items2/", tags=[Tags.items])
async def get_items():
    return ["Portal gun", "Plumus"]


@app.get("/users2/", tags=[Tags.users])
async def get_users():
    return ["Rick", "Morty"]


# summary and description
@app.post(
    "/items2/",
    response_model=Item,
    summary="Create and item",
    tags=[Tags.items],
)
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item
