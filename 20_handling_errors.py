from fastapi import FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler
from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import BaseModel

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
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    When a request contains invalid data, FastAPI internally raises a RequestValidationError.
    RequestValidationError is a sub-class of Pydantic's ValidationError.
    """
    errors = exc.errors()
    body = exc.body
    print(
        f"{errors=}"
    )  # [{'type': 'int_parsing', 'loc': ('body', 'size'), 'msg': 'Input should be a valid integer, unable to parse string as an integer', 'input': '12d3', 'url': 'https://errors.pydantic.dev/2.5/v/int_parsing'}]
    print(f"{body=}")  # {'title': 'string', 'size': '12d3'}
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": errors, "body": body}),
    )
    # return PlainTextResponse(str(exc), status_code=400)


# Override the HTTPException error handler
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    """
    FastAPI's HTTPException vs Starlette's HTTPException
    The only difference, is that FastAPI's HTTPException allows you to add headers to be included in the response.
    This is needed/used internally for OAuth 2.0 and some security utilities.
    """
    print(f"{request=}")  # <starlette.requests.Request object at 0x10cab0b90>
    print(f"{exc=}")  # HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.get("/items2/{item_id}")
async def read_item2(item_id: int, q: str):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}


class Item(BaseModel):
    title: str
    size: int


# Use the RequestValidationError body
@app.post("/items3/")
async def create_item(item: Item):
    return item


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)


# Re-use FastAPI's exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """
    If you want to use the exception along with the same default exception handlers from FastAPI
    You can import and re-use the default exception handlers from fastapi.exception_handlers
    """
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)
