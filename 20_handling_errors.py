from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(status_code=418, content={"message": f"Opps! {exc.name} did something"})


# Use HTTPException & Add custom headers
@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404, detail={"message": "Item not found"}, headers={"X-Error": "There goes my error"}
        )
    return {"item": items[item_id]}


# Install custom exception handlers
@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}
