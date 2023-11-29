from typing import Annotated

from fastapi import FastAPI
from fastapi.params import Body, Path
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


# Mix Path, Query and body parameters
@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: Annotated[int, Path(title="The ID of the item", ge=0, le=1000)],  # optional
    q: str | None = None,  # optional
    item: Item,  # required
):
    result = {"item_id": item_id}
    if q:
        result |= {"q": q}
    if item:
        result |= {"item": item}
    return result


# Multiple body parameters
@app.put("/items2/{item_id}")
async def update_item2(item_id: int, item: Item, user: User):  # required item & user
    """
    Request Body Example
    {
        "item": {
            "name": "Foo",
            "description": "The pretender",
            "price": 42.0,
            "tax": 3.2
        },
        "user": {
            "username": "dave",
            "full_name": "Dave Grohl"
        }
    }
    """
    return {"item_id": item_id, "item": item, "user": user}


# Singular values in body
@app.put("/items3/{item_id}")
async def update_item3(item_id: int, item: Item, user: User, importance: Annotated[int, Body()]):
    """
    by default, singular values are interpreted as query parameters
    you don't have to explicitly add a Query, you can just do:

    Request Body Example
    {
        "item": {
            "name": "Foo",
            "description": "The pretender",
            "price": 42.0,
            "tax": 3.2
        },
        "user": {
            "username": "dave",
            "full_name": "Dave Grohl"
        },
        "importance": 5
    }
    """
    return {"item_id": item_id, "item": item, "user": user, "importance": importance}


# Embed a single body parameter
@app.put("/items4/{item_id}")
async def update_item4(item_id: int, item: Annotated[Item, Body(embed=True)]):
    """
    Request Body Example
    {
        "item": {
            "name": "Foo",
            "description": "The pretender",
            "price": 42.0,
            "tax": 3.2
        }
    }
    """
    return {"item_id": item_id, "item": item}
