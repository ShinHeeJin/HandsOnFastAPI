from typing import Annotated

from fastapi import Body, FastAPI, File, Form, HTTPException, Path, Query, Request, status, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]


# Update replacing with PUT
@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    """
    Request
    - item_id : bar
    - json :
    {
        "name": "Barz",
        "price": 3,
        "description": None,
    }

    * it doesn't include the already stored attribute "tax": 20.2,
    the input model would take the default value of "tax": 10.5.
    """
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded


# Using Pydantic's update parameter
@app.patch("/items2/{item_id}", response_model=Item)
async def update_item2(item_id: str, item: Item):
    # item = Item(name='updated foo', description=None, price=None, tax=10.5, tags=[])

    stored_item_data = items[item_id]
    # stored_item_data = {'name': 'Foo', 'price': 50.2}

    stored_item_model = Item(**stored_item_data)
    # stored_item_model = Item(name='Foo', description=None, price=50.2, tax=10.5, tags=[])

    update_data = item.model_dump(exclude_unset=True)
    # update_data = {'name': 'updated foo'}

    updated_item = stored_item_model.model_copy(update=update_data)
    # updated_item = Item(name='updated foo', description=None, price=50.2, tax=10.5, tags=[])

    items[item_id] = jsonable_encoder(updated_item)
    return updated_item
