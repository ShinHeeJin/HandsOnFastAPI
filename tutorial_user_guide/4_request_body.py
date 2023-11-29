from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None  # Use None to make it just optional.


app = FastAPI()


# body data using Pydantic BaseModel
@app.post("/items/{item_id}")
async def create_item(item: Item, item_id: int, q: str | None = None):
    """
    Request json : {"name": "Foo","price": 45.3}
    Response json : {"name": "Foo","description": null,"price": 45.3,"tax": null}
    """
    item_dict: dict = item.model_dump()
    item_dict.update({"item_id": item_id})
    if item.tax:
        price = item.price + item.tax
        item_dict.update({"price_with_tax": price})
    item_dict.update({"q": q})
    return item_dict
