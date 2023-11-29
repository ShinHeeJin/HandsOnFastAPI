# https://fastapi.tiangolo.com/tutorial/security/first-steps/
# In this example we are going to use OAuth2, with the Password flow, using a Bearer token

from typing import Annotated, Callable

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme: Callable = OAuth2PasswordBearer(tokenUrl="./token")
# tokenUrl that the client will use to send the username and password in order to get a token.
# oauth2_scheme is also a "callable". So, it can be used with Depends.


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
