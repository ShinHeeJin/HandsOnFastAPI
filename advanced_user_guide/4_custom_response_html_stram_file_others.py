# https://fastapi.tiangolo.com/advanced/custom-response/#use-orjsonresponse
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

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
