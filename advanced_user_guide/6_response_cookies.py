# Use a Response parameter
from datetime import timedelta

from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

app = FastAPI()


# Cookie Use a Response parameter
@app.post("/cookie-and-object/")
def create_cookie(response: Response):
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return {"message": "Come to the dark side, we have cookies"}


# Return a Response directly
@app.post("/cookie")
def create_cookie2():
    """
    https://www.starlette.io/responses/#set-cookie
    """
    content = {"message": "Come to the dark side, we have cookies"}
    response = JSONResponse(content=content)
    response.set_cookie(
        key="fakesession", value="fake-cookie-session-value", expires=timedelta(days=1)
    )
    return response
