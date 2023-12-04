# https://fastapi.tiangolo.com/advanced/sub-applications/
from fastapi import FastAPI

app = FastAPI()


# Top-level application
@app.get("/app")
def read_main():
    return {"message": "Hello from main app"}


subapi = FastAPI()


@subapi.get("/sub")
def read_sub():
    return {"message": "Hello from sub API"}


app.mount("/subapi", subapi)
