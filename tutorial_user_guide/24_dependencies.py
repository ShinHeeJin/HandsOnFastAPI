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


async def my_parameters(q: str | None, skip: int = 0, me: int = 100):
    return None


# Share Annotated dependencies
MyDependecy = Annotated[dict, Depends(my_parameters)]


@app.get("/me/")
async def read_me(commons: MyDependecy):
    """
    And you can declare dependencies with async def inside of normal def path operation functions,
    or def dependencies inside of async def path operation functions, etc.
    """
    assert commons is None
    return commons
