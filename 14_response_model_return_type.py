from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


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
