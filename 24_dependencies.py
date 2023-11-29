from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()


# It is just a function that can take all the same parameters that a path operation function can take:
async def common_parameters(q: str | None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    """
    And it has the same shape and structure that all your path operation functions have.
    You don't call it directly (don't add the parenthesis at the end), you just pass it as a parameter to Depends().
    """
    return commons


@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons
