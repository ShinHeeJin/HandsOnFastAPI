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
