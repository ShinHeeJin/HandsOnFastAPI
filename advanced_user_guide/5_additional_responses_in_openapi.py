from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel


class Item(BaseModel):
    id: str
    value: str


class Message(BaseModel):
    message: str


app = FastAPI()


@app.get("/items/{item_id}", response_model=Item, responses={404: {"model": Message}})
async def read_item(item_id: str):
    if item_id == "foo":
        return {"id": "foo", "value": "there goes my hero"}
    return JSONResponse(status_code=404, content={"message": "Item not found"})


# Additional media types for the main response
@app.get(
    "/items2/{item_id}",
    response_model=Item,
    responses={
        200: {"content": {"image/png": {}}, "description": "Return the JSON item or an image."}
    },
)
async def read_item2(item_id: str, img: bool | None = None):
    """
    You can use this same responses parameter to add different media types for the same main response.
    * Notice that you have to return the image using a FileResponse directly.
    """
    if img:
        return FileResponse("image.png", media_type="image/png")
    return {"id": item_id, "value": "there goes ym hero"}


# Combining information
@app.get(
    "/itemsd/{item_id}",
    response_model=Item,
    responses={
        404: {"model": Message, "description": "The item was not found"},
        200: {
            "description": "Item requested by ID",
            "content": {"application/json": {"example": {"id": "bar", "value": "The bar tenders"}}},
        },
    },
)
async def read_item3(item_id: str):
    if item_id == "foo":
        return {"id": "foo", "value": "there goes my hero"}
    return JSONResponse(status_code=404, content={"message": "Item not found"})
