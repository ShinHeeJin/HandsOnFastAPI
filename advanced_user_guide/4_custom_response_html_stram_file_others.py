# https://fastapi.tiangolo.com/advanced/custom-response/#use-orjsonresponse
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, ORJSONResponse

"""
For large responses, returning a Response directly is much faster than returning a dictionary.

if you are certain that the content that you are returning is serializable with JSON,
you can pass it directly to the response class and avoid the extra overhead that FastAPI
would have by passing your return content through the jsonable_encoder before passing it to the response class.

orjson is a fast, correct JSON library for Python.
It benchmarks as the fastest Python library for JSON and is more correct than the standard json library or other third-party libraries.
It serializes dataclass, datetime, numpy, and UUID instances natively.
"""
app = FastAPI()


# Use ORJSONResponse
@app.get("/items/", response_class=ORJSONResponse)
async def read_items():
    return ORJSONResponse([{"item_id": "Foo"}])


# HTML Response
@app.get("/items2/", response_class=HTMLResponse)
async def read_items2():
    """
    The parameter response_class will also be used to define the "media type" of the response.
    In this case, the HTTP header Content-Type will be set to text/html.
    And it will be documented as such in OpenAPI.
    """
    return """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """


# you can also override the response directly in your path operation
@app.get("/items3/")
async def read_items3():
    """
    A Response returned directly by your path operation function won't be documented in OpenAPI
    """
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
