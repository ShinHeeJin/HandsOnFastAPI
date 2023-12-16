import requests
from fastapi import APIRouter, FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()


class Invoice(BaseModel):
    id: str
    title: str | None = None
    customer: str
    total: float


class InvoiceEvent(BaseModel):
    description: str
    paid: bool


class InvoiceEventReceived(BaseModel):
    ok: bool


invoices_callback_router = APIRouter()


@invoices_callback_router.post(
    "{$callback_url}/invoices/{$request.body.id}", response_model=InvoiceEventReceived
)
def invoice_notification(body: InvoiceEvent):
    """
    1. It doesn't need to have any actual code, because your app will never call this code.
    2. The path can contain an `OpenAPI 3` expression
    """
    pass


@app.post("/invoices/", callbacks=invoices_callback_router.routes)
def create_invoice(invoice: Invoice, callback_url: HttpUrl | None = None):
    """
    Create an invoice.

    This will (let's imagine) let the API user (some external developer) create an
    invoice.

    And this path operation will:

    * Send the invoice to the client.
    * Collect the money from the client.
    * Send a notification back to the API user (the external developer), as a callback.
        * At this point is that the API will somehow send a POST request to the
            external API with the notification of the invoice event
            (e.g. "payment successful").


    This code won't be executed in your app, we only need it to document how that external API should look like.
    But, you already know how to easily create automatic documentation for an API with FastAPI

    """
    # Send the invoice, collect the money, send the notification (the callback)

    # SUDO code
    resp = requests.post(f"{callback_url}/invoices/{invoice.id}")
    assert resp.json() == {"ok": True}

    return {"msg": "Invoice received"}
