from functools import lru_cache
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

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
    return Settings()


@app.get("/info")
async def info(settings: Annotated[Settings, Depends(get_settings)]):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }


client = TestClient(app)


def get_settings_in_test():
    return Settings(admin_email="testing_admin@example.com")


app.dependency_overrides[get_settings] = get_settings_in_test


def test_app():
    response = client.get("/info")
    data = response.json()
    assert data == {
        "app_name": "Awesome API",
        "admin_email": "testing_admin@example.com",
        "items_per_user": 50,
    }
