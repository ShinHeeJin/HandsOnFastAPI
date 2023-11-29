# https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/
import random
from typing import Annotated

from fastapi import Cookie, Depends, FastAPI

app = FastAPI()


def query_executor(q: str | None = None):
    return q


def query_or_cookie_extractor(
    q: Annotated[str, Depends(query_executor)], last_query: Annotated[str | None, Cookie()] = None
):
    if last_query:
        return last_query
    return q


# Second dependency, "dependable" and "dependant"
@app.get("/items/")
async def read_query(query_or_default: Annotated[str, Depends(query_or_cookie_extractor)]):
    """
    Notice that we are only declaring one dependency in the path operation function, the query_or_cookie_extractor.
    But FastAPI will know that it has to solve query_extractor first, to pass the results of that to query_or_cookie_extractor while calling it.
    """
    return {"q_or_cookie": query_or_default}


async def get_random_value():
    print("get_random_value")
    return random.choice([1, 2, 3])


async def generate_value(value: Annotated[int, Depends(get_random_value, use_cache=False)]):
    if value:
        return value
    return None


@app.get("/first")
async def first(
    value: Annotated[str, Depends(generate_value)],
    value2: Annotated[str, Depends(generate_value)],
):
    return value, value2
