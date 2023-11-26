from fastapi import FastAPI

app = FastAPI()


# Query Parameters
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    """
    Request: http://127.0.0.1:8000/items/?skip=1&limit=4
    Response: [1, 4]
    """
    return skip, limit


# Optional parameters
@app.get("/items/{item_id}")
async def read_item2(item_id: str, q: str | None = None):
    """
    Request: http://127.0.0.1:8000/items/test
    Response: {"item_id": "test", "q": null}
    """
    if q is not None:
        return {"q": q}
    return {"item_id": item_id, "q": q}


# Query parameter type conversion
@app.get("/items3/{item_id}")
async def read_item3(item_id: str, q: str | None = None, short: bool = False):
    """
    bool types converted
    on, 1, True, true, yes -> True
    """
    return {"item_id": item_id, "short": short}


# Multiple path and query parameters
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(item_id: str, user_id: int, q: str | None = None, short: bool = False):
    return {
        "user_id": user_id,
        "item_id": item_id,
        "q": q,
        "short": short,
    }
