# https://fastapi.tiangolo.com/advanced/behind-a-proxy/
"""
The root_path is a mechanism provided by the ASGI specification (that FastAPI is built on, through Starlette).

The root_path is used to handle these specific cases.

And it's also used internally when mounting sub-applications.
"""

# check root_path

from fastapi import FastAPI, Request

app = FastAPI()


# uvicorn main:app --root-path /api/v1
@app.get("/app")
def read_main(request: Request):
    root_path = request.scope.get("root_path")  # "/api/v1"
    return {"message": "Hello World", "root_path": root_path}
