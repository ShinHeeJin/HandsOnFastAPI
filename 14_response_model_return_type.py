from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


@app.post("/items/")
async def create_item(item: Item) -> Item:
    return item


# Response Model - Return Type
@app.get("/items/")
async def read_items() -> list[Item]:
    """
    1. Validate the returned data,
    2. Add a JSON Schema for the response, in the OpenAPI path operation
    """
    return [Item(name="Portal Gun", price=52.0), Item(name="Plumbus", price=32.0)]


# response_model Parameter
@app.get("/items2", response_model=list[Item])
async def read_items2() -> Any:
    return [
        {"name": "Portal Gun", "price": 52.0},
        {"name": "Plumbus", "price": 32.0},
    ]


# Return the same input data
@app.post("/user/")
async def create_user(user: UserIn) -> UserIn:
    return user


# Add an output model
@app.post("/user2/", response_model=UserOut)
async def create_user2(user: UserIn) -> Any:
    return user
