from fastapi import FastAPI, Response

app = FastAPI()


# Use a Response parameter
@app.get("/headers-and-object/")
async def get_headers(response: Response):
    """
    Response Header
        content-length: 25
        content-type: application/json
        date: Thu,30 Nov 2023 16:40:05 GMT
        server: uvicorn
        x-cat-dog: alone in the world
    """
    response.headers["X-Cat-Dog"] = "alone in the world"
    return {"message": "Hello world"}
