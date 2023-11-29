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
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    response.update({"items": fake_items_db[commons.skip : commons.skip + commons.limit]})
    return None
