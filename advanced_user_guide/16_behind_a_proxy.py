# https://fastapi.tiangolo.com/advanced/behind-a-proxy/
"""
The root_path is a mechanism provided by the ASGI specification (that FastAPI is built on, through Starlette).

The root_path is used to handle these specific cases.

And it's also used internally when mounting sub-applications.
"""

# check root_path

from fastapi import FastAPI, Request

app = FastAPI(root_path="/api/v1")


# uvicorn main:app --root-path /api/v1
@app.get("/app")
def read_main(request: Request):
    """
    But if you go with your browser to http://127.0.0.1:8000/app you will see the normal response:
    So, it won't expect to be accessed at http://127.0.0.1:8000/api/v1/app.
    Uvicorn will expect the proxy to access Uvicorn at http://127.0.0.1:8000/app, and then it would be the proxy's responsibility to add the extra /api/v1 prefix on top.
    """
    root_path = request.scope.get("root_path")  # "/api/v1"
    return {"message": "Hello World", "root_path": root_path}
