from fastapi.testclient import TestClient

from .main import app

"""
HTTPX's design is based on Requests' design.

To pass a path or query parameter, add it to the URL itself.
To pass a JSON body, pass a Python object (e.g. a dict) to the parameter json.
If you need to send Form Data instead of JSON, use the data parameter instead.
To pass headers, use a dict in the headers parameter.
For cookies, a dict in the cookies parameter.

"""
client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_read_item():
    response = client.get("/items/foo", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == {"id": "foo", "title": "Foo", "description": "There goes my hero"}


def test_read_item_bad_token():
    response = client.get("/items/foo", headers={"X-Token": "hailhydra"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_read_inexistent_item():
    response = client.get("/items/baz", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_create_item():
    response = client.post(
        "/items/", headers={"X-Token": "coneofsilence"}, json={"id": "foobar", "title": "Foo Bar"}
    )
    assert response.status_code == 200
    assert response.json() == {"id": "foobar", "title": "Foo Bar", "description": None}


def test_create_item_bad_token():
    response = client.post(
        "/items/",
        headers={"X-Token": "hailhydra"},
        json={"id": "bazz", "title": "Bazz", "description": "Drop the bazz"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_create_existing_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={"id": "foo", "title": "The Foo ID Stealer"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Item already exists"}
