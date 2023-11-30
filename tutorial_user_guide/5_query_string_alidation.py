from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()


# Annotated
@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):  # q : optional
    result = dict()
    if q:
        result.update({"q": q})
    return result


# without Annotated
@app.get("/items2/")
async def read_items2(q: str | None = Query(default=None, max_length=50)):  # q : optional
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
    if q2:
        result.update({"q2": q2})
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
async def read_items5(
    q: Annotated[str | None, Query(min_length=3, max_length=10, pattern="^api_v\d+$")]
):
    return q


# Required with Ellipsis ( explicitly declare )
@app.get("/items6/")
async def read_items6(q: Annotated[str | None, Query(default=...)]):
    return q


# Query parameter list / multiple values
# http://127.0.0.1:8000/items7/?q=apple&q=banan
@app.get("/items7/")
async def read_items7(q: Annotated[list[str] | None, Query()] = ["banana", "apple"]):
    """cf) you need to explicitly use Query, otherwise it would be interpreted as a request body."""
    return {"q": q}


# metadata ( title & description )
@app.get("/items8/")
async def read_items8(
    q: Annotated[
        str | None,
        Query(
            title="Query String!",
            description="Query String for the items to saerch in data db",
            min_length=3,
        ),
    ] = None
):
    return {"q": q}


# Alias parameters
@app.get("/items9/")
async def read_items9(item_query: Annotated[str | None, Query(alias="item-query")] = None):
    """item-query ==> item_query"""
    return {"item_query": item_query}


# Deprecating parameters
@app.get("/items10/")
async def read_item10(
    item_query: Annotated[
        str | None,
        Query(
            alias="item-query",
            title="Query String ItemQuery",
            description="Query string for the items",
            min_length=3,
            max_length=50,
            deprecated=True,
        ),
    ] = None
):
    return {"item_query": item_query}


# Exclude from OpenAPI
# http://127.0.0.1:8000/items11/?hidden-query=1234
@app.get("/items11/")
async def read_items11(
    hidden_query: Annotated[str | None, Query(include_in_schema=False, alias="hidden-query")] = None
):
    if hidden_query:
        return {"hidden_query": hidden_query}
    return {}
