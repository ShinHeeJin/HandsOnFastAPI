from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str = Field(title="itemName", examples=["BAG"])
    description: str | None = Field(
        default=None,
        title="The description of the item",
        min_length=5,
        max_length=300,
        examples=["item description"],
    )
    price: float = Field(
        gt=0,
        lt=99999,
        title="Item Price",
        description="The price must be greater than zero",
        examples=[1200],
    )
    tax: float | None = Field(
        default=None, title="itemTax", examples=[0.5], ge=0, le=99999, description="item Tax"
    )


# Body - Fields
@app.get("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    return {"item_id": item_id, "item": item}
