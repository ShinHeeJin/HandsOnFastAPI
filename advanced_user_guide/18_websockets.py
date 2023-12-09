from typing import Annotated

from fastapi import (
    Cookie,
    Depends,
    FastAPI,
    Query,
    WebSocket,
    WebSocketDisconnect,
    WebSocketException,
    status,
)
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# http://127.0.0.1:8000/static/websocket.html
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")


async def get_cookie_or_token(
    websocket: WebSocket,
    session: Annotated[str | None, Cookie()] = None,
    token: Annotated[str | None, Query] = None,
):
    if session is None and token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return session or token


# Using Depends and others
@app.websocket("/items/{item_id}/ws")
async def websocket_endpoint2(
    *,
    websocket: WebSocket,
    item_id: str,
    q: int | None = None,
    cookie_or_token: Annotated[str, Depends(get_cookie_or_token)],
):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Session cookie or query token valud is : {cookie_or_token}")
        if q is not None:
            await websocket.send_text(f"Query p is : {q}")

        await websocket.send_text(f"Message text was: {data}, for item ID: {item_id}")


# Handling disconnections and multiple clients
class ConnectionManager:
    def __init__(self) -> None:
        self.avtive_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.avtive_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.avtive_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.avtive_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint3(websocket: WebSocket, client_id: int):
    """
    When a WebSocket connection is closed, the await websocket.receive_text() will raise a WebSocketDisconnect exception
    which you can then catch and handle like in this example.
    """
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
