from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()


# Annotated
@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
    result = dict()
    if q:
        result.update({"q": q})
    return result


# without Annotated
@app.get("/items2/")
async def read_items2(q: str | None = Query(default=None, max_length=50)):
    result = dict()
    if q:
        result.update({"q": q})
    return result
