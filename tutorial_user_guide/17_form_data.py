from typing import Annotated

from fastapi import FastAPI, Form

app = FastAPI()


# Define Form parameters
@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    """
    Data from forms is normally encoded using the "media type" application/x-www-form-urlencoded.
    But when the form includes files, it is encoded as multipart/form-data. You'll read about handling files in the next chapter.
    """
    return {"username": username}
