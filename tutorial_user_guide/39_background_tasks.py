from typing import Annotated

from fastapi import (
    BackgroundTasks,
    Depends,
    FastAPI,
)

"""
The class BackgroundTasks comes directly from starlette.background.
It's still possible to use BackgroundTask alone in FastAPI,
but you have to create the object in your code and return a Starlette Response including it.

If you need to perform heavy background computation and you don't necessarily need it to be run by the same process
(for example, you don't need to share memory, variables, etc), you might benefit from using other bigger tools like Celery.
"""

app = FastAPI()


def write_notification(email: str, message=""):
    """
    email -> positional argument
    message -> keyword argument
    It can be an async def or normal def function
    """
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email} : {message}"
        email_file.write(content)


@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}


# Dependency Injection system
def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(f"{message}")


def get_query(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q


@app.post("/send-notification2/{email}")
async def send_notification2(
    email: str, background_tasks: BackgroundTasks, q: Annotated[str, Depends(get_query)]
):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent"}
