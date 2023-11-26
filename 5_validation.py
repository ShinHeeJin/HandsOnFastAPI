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
