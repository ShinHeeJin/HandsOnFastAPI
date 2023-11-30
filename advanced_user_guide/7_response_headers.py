from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI()


class Message(BaseModel):
    message: str = Field(
        title="message", description="This is Success Message", examples=["success!!"]
    )


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


# Return a Response directly
@app.get(
    "/headers/",
    responses={
        200: {
            "model": Message,
            "description": "hello world!!",
            "content": {"application/json": {"example": {"message": "Hello world"}}},
        },
    },
)
def get_headers2():
    content = {"message": "Hello world"}
    headers = {"X-Cat-Dog": "alone in the world", "Content-Language": "en-US"}
    return JSONResponse(content=content, headers=headers)
