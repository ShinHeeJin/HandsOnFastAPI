from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}


# Use HTTPException & Add custom headers
@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404, detail={"message": "Item not found"}, headers={"X-Error": "There goes my error"}
        )
    return {"item": items[item_id]}
