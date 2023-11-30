import yaml
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.routing import APIRoute
from pydantic import BaseModel, ValidationError

app = FastAPI()


@app.get("/items/", operation_id="some_specific_id_you_define")
async def read_items():
    return [{"item_id": "Foo"}]


@app.get("/items2/", include_in_schema=False)
async def read_items2():
    return [{"item_id": "Foo"}]


@app.post("/items3/{item_id}", summary="Create an item")
async def create_item(item_id: int):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    \f
    :param item_id: Item Id ( User input )
    """
    return {}


@app.get("/items4/", openapi_extra={"x-aperture-labs-portal": "red"})
async def read_items3():
    return [{"item_id": "portal-gun"}]


class Item(BaseModel):
    name: str
    tags: list[str]


# Custom OpenAPI content type
@app.post(
    "/items2/",
    openapi_extra={
        "requestBody": {
            "content": {"application/x-yaml": {"schema": Item.model_json_schema()}},
            "required": True,
        }
    },
)
async def create_item2(request: Request):
    raw_body: bytes = await request.body()
    # raw_body=b'name: string\ntags:\n  - string'
    try:
        data = yaml.safe_load(raw_body)
        # data={'name': 'string', 'tags': ['string']}
    except yaml.YAMLError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Ivalid YAML")

    try:
        item = Item.model_validate(data)
        # item = Item(name='string', tags=['string'])
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.errors())
    return item


def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        """
        route
        Route(path='/openapi.json', name='openapi', methods=['GET', 'HEAD'])
        Route(path='/docs', name='swagger_ui_html', methods=['GET', 'HEAD'])
        Route(path='/docs/oauth2-redirect', name='swagger_ui_redirect', methods=['GET', 'HEAD'])
        Route(path='/redoc', name='redoc_html', methods=['GET', 'HEAD'])
        APIRoute(path='/items/', name='read_items', methods=['GET'])
        """
        if isinstance(route, APIRoute):
            route.operation_id = route.name  # in this case, 'read_items'


use_route_names_as_operation_ids(app)
