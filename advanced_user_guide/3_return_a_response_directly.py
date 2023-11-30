from datetime import datetime

from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None


app = FastAPI()


# Using the jsonable_encoder in a Response
@app.put("/items/{id}")
def update_item(id: str, item: Item):
    """
    you can return a JSONResponse directly from your path operations.
    when you return a Response, FastAPI will pass it directly. It won't do any data conversion with Pydantic models
    """
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(item))
