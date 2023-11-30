# https://fastapi.tiangolo.com/tutorial/static-files/
# https://www.starlette.io/staticfiles/

from fastapi import (
    FastAPI,
)
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", app=StaticFiles(directory="static"), name="heejin")
