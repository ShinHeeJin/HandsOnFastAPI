from typing import Any

from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse, RedirectResponse
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


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(BaseUser):
    password: str


# Return Type and Data Filtering
@app.post("/user3")
async def create_user3(user: UserIn) -> BaseUser:
    """
    Request Samples
    {
        "username": "string",
        "email": "user@example.com",
        "full_name": "string",
        "password": "string"
    }

    Response Samples
    {
        "username": "string",
        "email": "user@example.com",
        "full_name": "string"
    }
    """
    return user


# Return a Response Directly
@app.get("/portal")
async def get_portal(teleport: bool = False) -> Response:
    if teleport:
        return RedirectResponse(url="http://127.0.0.1:8000/docs")
    return JSONResponse(content={"message": "Here's your interdimensional portal"})


# Disable Response Model
@app.get("/portal2", response_model=None)
async def get_portal2(teleport: bool = False) -> Response | dict:
    """
    This will make FastAPI skip the response model generation
    and that way you can have any return type annotations you need without it
    """
    if teleport:
        return RedirectResponse(url="http://127.0.0.1:8000/docs")
    return {"message": "Here's your interdimensional portal"}
