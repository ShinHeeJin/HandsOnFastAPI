# https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/
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
    return {"q_or_cookie": query_or_default}
