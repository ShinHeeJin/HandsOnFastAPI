from fastapi import FastAPI

app = FastAPI()


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    """
    Request: http://127.0.0.1:8000/items/?skip=1&limit=4
    Response: [1, 4]
    """
    return skip, limit


@app.get("/items/{item_id}")
async def read_item2(item_id: str, q: str | None = None):
    """
    Request: http://127.0.0.1:8000/items/test
    Response: {"item_id": "test", "q": null}
    """
    if q is not None:
        return {"q": q}
    return {"item_id": item_id, "q": q}
