from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/items/{item_id}")
async def read_root(item_id: str, request: Request):
    """
    https://www.starlette.io/requests/
    """
    client_host = request.client.host
    request.method
    request.url
    request.headers
    request.query_params
    request.path_params
    request.cookies
    await request.body()
    await request.json()
    await request.form()
    return {"client_host": client_host, "item_id": item_id}
