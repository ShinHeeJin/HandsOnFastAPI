from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from flask import Flask, request

"""
You can mount WSGI applications as you saw with Sub Applications - Mounts, Behind a Proxy.
For that, you can use the WSGIMiddleware and use it to wrap your WSGI application, for example, Flask, Django, etc.
"""

flask_app = Flask(__name__)


@flask_app.route("/")
def flask_main():
    name = request.args.get("name", "unknown")
    return f"Hello, {name} from Flask"


app = FastAPI()


@app.get("/v2")
def read_main():
    return {"message": "Hello FastAPI"}


app.mount("/v1", WSGIMiddleware(flask_app))
