from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

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


# Override the default exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """
    When a request contains invalid data, FastAPI internally raises a RequestValidationError.
    RequestValidationError is a sub-class of Pydantic's ValidationError.
    """
    return PlainTextResponse(str(exc), status_code=400)


# Override the HTTPException error handler
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    print(f"{request=}")  # <starlette.requests.Request object at 0x10cab0b90>
    print(f"{exc=}")  # HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.get("/items2/{item_id}")
async def read_item2(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}
