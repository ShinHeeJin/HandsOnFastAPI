# Use a Response parameter

from fastapi import FastAPI, Response

app = FastAPI()


# Cookie Use a Response parameter
@app.post("/cookie-and-object/")
def create_cookie(response: Response):
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return {"message": "Come to the dark side, we have cookies"}
