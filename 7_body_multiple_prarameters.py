from typing import Annotated

from fastapi import FastAPI, Path
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


# Mix Path, Query and body parameters
@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item", ge=0, le=1000)],
    q: str | None = None,
    item: Item | None = None,
):
    result = {"item_id": item_id}
    if q:
        result |= {"q": q}
    if item:
        result |= {"item": item}
    return None
