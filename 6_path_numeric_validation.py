from typing import Annotated

from fastapi import FastAPI, Path, Query

app = FastAPI()


# Path ( title )
@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item")],
    item_query: Annotated[str | None, Query(alias="item-query")] = None,
):
    result = {"item_id": item_id}
    if item_query:
        result |= {"item_query": item_query}
    return result


# Number validations: greater than or equal, less than or equal
@app.get("/items2/{item_id}")
async def read_items2(item_id: Annotated[int, Path(title="The ID of the item", ge=1, le=999)], query: str):
    result = {"item_id": item_id}
    if query:
        result |= {"query": query}
    return result


# Number validations: floats, greater than and less than
@app.get("/items3/{item_id}")
async def read_items3(
    *,
    query: str,
    size: Annotated[float, Query(gt=0, lt=10.5)],
    item_id: Annotated[int, Path(title="The ID of the item", ge=0, le=1000)],
):
    result = {"item_id": item_id}
    result = result | {"query": query}
    result |= {"size": size}
    print
    return result
