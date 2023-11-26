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


# without Annotated
@app.get("/items2/")
async def read_items2(q: str | None = Query(default=None, max_length=50)):
    result = dict()
    if q:
        result.update({"q": q})
    return result


# Query as the default value or in Annotated
@app.get("/items3/")
async def read_items3(
    q1: str | None = Query(default="rick"),
    q2: Annotated[str, Query()] = "rick",
):
    result = dict()
    if q1:
        result.update({"q1": q1})
    return result


# add more validations
@app.get("/items4/")
async def read_items4(q: Annotated[str | None, Query(min_length=3, max_length=50)] = None):
    result = dict()
    if q:
        result.update({"q": q})
    return result


# Add regular expressions
@app.get("/items5/")
async def read_items5(q: Annotated[str | None, Query(min_length=3, max_length=10, pattern="^api_v\d+$")]):
    return q


# Required with Ellipsis ( explicitly declare )
@app.get("/items6/")
def read_items6(q: Annotated[str | None, Query(default=..., min_length=3)]):
    return q
