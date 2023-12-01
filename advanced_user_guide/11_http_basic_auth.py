# https://fastapi.tiangolo.com/advanced/security/http-basic-auth/
import secrets
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
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


# Check the username
def get_current_username(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    current_user_name_bytes = credentials.username.encode("utf8")
    correct_user_name_bytes = b"stanleyjobson"
    is_correct_username = secrets.compare_digest(current_user_name_bytes, correct_user_name_bytes)
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"swordfish"
    is_correct_password = secrets.compare_digest(current_password_bytes, correct_password_bytes)

    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/users2/me")
def read_current_user2(username: Annotated[str, Depends(get_current_username)]):
    """
    Request Headers
        Authorization: Basic c3RhbmxleWpvYnNvbjpzd29yZGZpc2g=
        User-Agent: PostmanRuntime/7.32.1
        Accept: */*
        Cache-Control: no-cache
        Postman-Token: 671908fd-89bc-47d3-a30b-97b6d2b896a4
        Host: 127.0.0.1:8000
        Accept-Encoding: gzip, deflate, br
        Connection: keep-alive

    Response Headers
        date: Fri, 01 Dec 2023 08:47:10 GMT
        server: uvicorn
        content-length: 28
        content-type: application/json
    Response Body
        {"username":"stanleyjobson"}
    """
    return {"username": username}
