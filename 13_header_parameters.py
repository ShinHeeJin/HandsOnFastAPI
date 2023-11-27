from typing import Annotated

from fastapi import FastAPI, Header

app = FastAPI()


# Declare Header parameters
@app.get("/items/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}


# Duplicate headers
@app.get("/items2/")
async def read_items2(x_token: Annotated[list[str] | None, Header()] = None):
    return {"X-Token values": x_token}
