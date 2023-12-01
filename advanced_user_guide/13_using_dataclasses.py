from dataclasses import dataclass

from fastapi import FastAPI


@dataclass
class Item:
    name: str
    price: float
    description: str | None = None
    tax: float | None = None


app = FastAPI()


# Using Dataclasses
@app.post(
    "/items/",
    response_model=Item,
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {"name": "item", "price": 10.5, "description": "my item", "tax": 0.5}
                }
            },
            "description": "description of items",
        }
    },
)
async def create_item(item: Item):
    """
    This is still supported thanks to Pydantic, as it has internal support for dataclasses.
    So, even with the code above that doesn't use Pydantic explicitly,
    FastAPI is using Pydantic to convert those standard dataclasses to Pydantic's own flavor of dataclasses.
    """
    return item
