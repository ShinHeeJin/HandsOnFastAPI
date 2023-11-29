from datetime import datetime

from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from pydantic import BaseModel

fake_db = {}


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None


app = FastAPI()


# Using the jsonable_encoder
@app.put("/items/{id}")
async def update_item(id: str, item: Item):
    encoded = jsonable_encoder(item)
    # tem = Item(title='string', timestamp=datetime.datetime(2023, 11, 29, 2, 26, 46, 332000, tzinfo=TzInfo(UTC)), description='string')
    print(f"{item = }")
    # encoded = {'title': 'string', 'timestamp': '2023-11-29T02:26:46.332000Z', 'description': 'string'}
    print(f"{encoded = }")
    fake_db[id] = encoded
    return Response(status_code=status.HTTP_201_CREATED)
