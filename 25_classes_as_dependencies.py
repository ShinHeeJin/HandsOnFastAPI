# https://fastapi.tiangolo.com/tutorial/dependencies/classes-as-dependencies/

from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()

"""
The key factor is that a dependency should be a "callable".
Then, in FastAPI, you could use a Python class as a dependency.
"""


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class CommonQueryParams:
    """
    Pay attention to the __init__ method used to create the instance of the class:
    it has the same parameters as our previous common_parameters:
    """

    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


# Classes as dependencies
@app.get("/items/")
async def read_items(commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]):
    """
    the first CommonQueryParams doesn't have any special meaning for FastAPI.
    FastAPI won't use it for data conversion, validation, etc.
    You could actually write just

    ```python
    commons: Annotated[Any, Depends(CommonQueryParams)]
    ```

    But declaring the type is encouraged as that way your editor will know what will be passed
    as the parameter commons, and then it can help you with code completion, type checks, etc:
    """
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    response.update({"items": fake_items_db[commons.skip : commons.skip + commons.limit]})
    return response


# Shortcut
@app.get("/items")
async def read_items2(commons: Annotated[CommonQueryParams, Depends()]):
    """
    You declare the dependency as the type of the parameter, and you use Depends() without any parameter,
    instead of having to write the full class again inside of Depends(CommonQueryParams).
    """
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    response.update({"items": fake_items_db[commons.skip : commons.skip + commons.limit]})
    return response
