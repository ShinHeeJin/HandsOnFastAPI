# https://fastapi.tiangolo.com/advanced/security/http-basic-auth/
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

security = HTTPBasic()


@app.get("/users/me")
def read_current_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    """
    In HTTP Basic Auth, the application expects a header that contains a username and a password.
    And returns a header WWW-Authenticate with a value of Basic, and an optional realm parameter.
    """
    return {"username": credentials.username, "password": credentials.password}
