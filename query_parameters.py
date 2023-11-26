from fastapi import FastAPI

app = FastAPI()


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    """
    Request: http://127.0.0.1:8000/items/?skip=1&limit=4
    Response : [1, 4]
    """
    return skip, limit
