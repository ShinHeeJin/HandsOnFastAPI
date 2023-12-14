# https://fastapi.tiangolo.com/advanced/async-tests/
# Being able to use asynchronous functions in your tests could be useful, for example, when you're querying your database asynchronously

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Tomato"}
