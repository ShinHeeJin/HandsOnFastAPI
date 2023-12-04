from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI()

app.add_middleware(HTTPSRedirectMiddleware)
"""Enforces that all incoming requests must either be https or wss.
Any incoming requests to http or ws will be redirected to the secure scheme instead."""


app.add_middleware(TrustedHostMiddleware, allowed_hosts=["example.com", "*.example.com"])
"""Enforces that all incoming requests have a correctly set Host header, in order to guard against HTTP Host Header attacks.
If an incoming request does not validate correctly then a 400 response will be sent."""

app.add_middleware(GZipMiddleware, minimum_size=1000)
"""Handles GZip responses for any request that includes "gzip" in the Accept-Encoding header.
네트워크 대역폭 절약 및 성능 향상을 위하 gzip으로 응답을 압축"""

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=600,  # default 600, maximum time in seconds for browsers to cache CORS responses
)

app.add_middleware(CORSMiddleware)

# others
# https://github.com/florimondmanca/awesome-asgi
# https://docs.sentry.io/platforms/python/integrations/fastapi/
# https://github.com/florimondmanca/msgpack-asgi
# https://github.com/encode/uvicorn/blob/master/uvicorn/middleware/proxy_headers.py
# https://github.com/abersheeran/asgi-ratelimit
# https://github.com/snok/asgi-correlation-id
# https://github.com/steinnes/timing-asgi
# https://github.com/aogier/starlette-authlib


@app.get("/")
async def main():
    return {"message": "Hello World"}
