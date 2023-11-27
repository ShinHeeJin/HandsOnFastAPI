from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()


class Image(BaseModel):
    # The string will be checked to be a valid URL, and documented in JSON Schema / OpenAPI as such.
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    # if you receive a request with duplicate data, it will be converted to a set of unique items.
    tags: set[str] = set()
    images: list[Image] | None = None


class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]


# Set types &  Nested Models
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    """
    This would mean that FastAPI would expect a body similar to:
    {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2,
        "tags": ["rock", "metal", "bar"],
        "image": {
            "url": "http://example.com/baz.jpg",
            "name": "The Foo live"
        }
    }
    """
    return {"item_id": item_id, "item": item}


# Deeply nested models
@app.post("/offers/")
async def create_offer(offer: Offer):
    """
    {
        "name": "string",
        "description": "string",
        "price": 0,
        "items": [
            {
            "name": "string",
            "description": "string",
            "price": 0,
            "tax": 0,
            "tags": [],
            "images": [
                {
                "url": "http://example.com",
                "name": "string"
                }
            ]
            }
        ]
    }

    """
    return offer


# Bodies of pure lists
@app.post("/images/multiple")
async def create_multiple_images(images: list[Image]):
    return images


# Bodies of arbitrary dicts
@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    """
    This would be useful if you want to receive keys that you don't already know
    Another useful case is when you want to have keys of another type (e.g., int).
    {
        "1": 0.2,
        "2": 0.3
    }
    """
    return weights
