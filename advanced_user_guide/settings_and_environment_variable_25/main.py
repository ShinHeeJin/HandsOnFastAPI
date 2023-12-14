from functools import lru_cache
from typing import Annotated

from fastapi import Depends, FastAPI

from .config import Settings

# class Settings(BaseSettings):
#     """
#     Pydantic will read the environment variables in a case-insensitive way, so, an upper-case variable APP_NAME will still be read for the attribute app_name.

#     command: ADMIN_EMAIL="deadpool@example.com" APP_NAME="ChimichangApp" uvicorn 25_settings_and_environment_variables:app --reload
#     """

#     app_name: str = "Awesome API"
#     admin_email: str
#     items_per_user: int = 50

app = FastAPI()


@lru_cache
def get_settings():
    """
    But as we are using the @lru_cache decorator on top, the Settings object will be created only once, the first time it's called. ✔️
    it will return the same object that was returned on the first call, again and again.
    """
    return Settings()


@app.get("/info")
async def info(settings: Annotated[Settings, Depends(get_settings)]):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }
