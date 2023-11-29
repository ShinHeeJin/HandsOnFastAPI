# https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/


from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, status

app = FastAPI()


async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="X-token header invalid")


async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="X-Key header invalid")
    return x_key


# Dependencies in path operation decorators
@app.get("/items/", dependencies=[Depends(verify_key), Depends(verify_token)])
async def read_items():
    """
    Add dependencies to the path operation decorator
    These dependencies will be executed/solved the same way as normal dependencies.
    But their value (if they return any) won't be passed to your path operation function.
    """
    return [{"item": "Foo"}, {"item": "Bar"}]
