from typing import Annotated

from fastapi import Cookie, FastAPI

app = FastAPI()


# Declare Cookie parameters
@app.get("/items/")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}
