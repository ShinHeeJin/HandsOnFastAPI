from fastapi import FastAPI
from fastapi.routing import APIRoute

app = FastAPI()


@app.get("/items/", operation_id="some_specific_id_you_define")
async def read_items():
    return [{"item_id": "Foo"}]


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
