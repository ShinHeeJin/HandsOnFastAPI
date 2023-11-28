from http import HTTPStatus

from fastapi import FastAPI

app = FastAPI()


# Response Status Code
@app.post("/items/", status_code=HTTPStatus.CREATED)
async def create_item(name: str):
    return {"name": name}
