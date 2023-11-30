# https://fastapi.tiangolo.com/advanced/custom-response/#use-orjsonresponse
from typing import Any

import orjson
from fastapi import FastAPI, Response
from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    ORJSONResponse,
    RedirectResponse,
    StreamingResponse,
)

"""
For large responses, returning a Response directly is much faster than returning a dictionary.

if you are certain that the content that you are returning is serializable with JSON,
you can pass it directly to the response class and avoid the extra overhead that FastAPI
would have by passing your return content through the jsonable_encoder before passing it to the response class.

orjson is a fast, correct JSON library for Python.
It benchmarks as the fastest Python library for JSON and is more correct than the standard json library or other third-party libraries.
It serializes dataclass, datetime, numpy, and UUID instances natively.
"""
# Default response class
app = FastAPI(default_response_class=ORJSONResponse)


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


# Return an HTMLResponse directly
@app.get("/items4/", response_class=HTMLResponse)
async def read_items4():
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


# RedirectResponse
@app.get("/typer")
async def redirect_typer():
    """
    Returns an HTTP redirect. Uses a 307 status code (Temporary Redirect) by default.
    """
    return RedirectResponse("http://localhost:8000/docs")


# RedirectResponse2
@app.get("/typer2", response_class=RedirectResponse, status_code=302)
async def redirect_typer2():
    return "http://localhost:8000/docs"


async def fake_video_streamer():
    for i in range(50):
        yield b"some fake video bytes"


# StreamingResponse
@app.get("/video")
async def main():
    return StreamingResponse(fake_video_streamer())


@app.get("/file")
def file():
    """
    Response Header
        content-type: video/mp4
        date: Thu,30 Nov 2023 14:18:52 GMT
        server: uvicorn
        transfer-encoding: chunked
    """

    def iter_file(path):
        with open(path, mode="rb") as file_like:
            """
            This yield from tells the function to iterate over that thing named file_like. And then, for each part iterated, yield that part as coming from this generator function.
            So, it is a generator function that transfers the "generating" work to something else internally.
            By doing it this way, we can put it in a with block, and that way, ensure that it is closed after finishing.
            """
            yield from file_like

    return StreamingResponse(iter_file("./data/test.mp4"), media_type="video/mp4")


# FileResponse
@app.get("/file2")
async def file2():
    """
    Response Header
        content-disposition: attachment; filename="testttt.mp4"
        content-length: 316731
        content-type: video/mp4
        custom-header: test
        date: Thu,30 Nov 2023 14:32:07 GMT
        etag: 0d53983dfcd4308cc1d46c987435c4c9
        last-modified: Thu,30 Nov 2023 14:17:42 GMT
        server: uvicorn
    """
    return FileResponse(
        path="./data/test.mp4",
        headers={"Custom-Header": "test"},
        media_type="video/mp4",
        filename="testttt.mp4",
    )


@app.get("/file3", response_class=FileResponse)
async def file3():
    """
    Response Header
        content-length: 316731
        content-type: video/mp4
        date: Thu,30 Nov 2023 14:31:52 GMT
        etag: 0d53983dfcd4308cc1d46c987435c4c9
        last-modified: Thu,30 Nov 2023 14:17:42 GMT
        server: uvicorn
    """
    return "./data/test.mp4"


class CustomORJSONResponse(Response):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        assert orjson is not None, "orjson must be installed"
        return orjson.dumps(content, option=orjson.OPT_INDENT_2)


@app.get("/custom-response", response_class=CustomORJSONResponse)
async def custom_response():
    return {"message": "Hello World"}
