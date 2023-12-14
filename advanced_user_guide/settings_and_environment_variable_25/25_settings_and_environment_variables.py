from fastapi import FastAPI

from .config import settings

# class Settings(BaseSettings):
#     """
#     Pydantic will read the environment variables in a case-insensitive way, so, an upper-case variable APP_NAME will still be read for the attribute app_name.

#     command: ADMIN_EMAIL="deadpool@example.com" APP_NAME="ChimichangApp" uvicorn 25_settings_and_environment_variables:app --reload
#     """

#     app_name: str = "Awesome API"
#     admin_email: str
#     items_per_user: int = 50

app = FastAPI()


@app.get("/info")
async def info():
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }
