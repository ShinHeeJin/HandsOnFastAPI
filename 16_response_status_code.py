from http import HTTPStatus

from fastapi import FastAPI, status

app = FastAPI()


# Response Status Code
@app.post("/items/", status_code=HTTPStatus.CREATED)
async def create_item(name: str):
    return {"name": name}


# Shortcut to remember the names
@app.post("/items2/", status_code=status.HTTP_201_CREATED)
async def create_item2(name: str):
    return {"name": name}
