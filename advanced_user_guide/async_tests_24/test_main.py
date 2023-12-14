import pytest
from httpx import AsyncClient

from .main import app


# The marker @pytest.mark.anyio tells pytest that this test function should be called asynchronously
@pytest.mark.anyio()
async def test_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Tomato"}
