from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Subscription(BaseModel):
    username: str
    monthly_fee: float
    start_date: datetime


@app.webhooks.post("new-subscription")  # will be used just for documentation of webhooks.
def new_subscription(body: Subscription):
    """
    When a new user subscribes to your service we'll send you a POST request with this
    data to the URL that you register for the event `new-subscription` in the dashboard.

    Notice that with webhooks you are actually not declaring a path (like /items/),
    the text you pass there is just an identifier of the webhook (the name of the event)
    """


@app.get("/users/")
def read_users():
    return ["Rick", "Morty"]
