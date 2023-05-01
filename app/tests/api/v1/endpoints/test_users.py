import pytest
from httpx import AsyncClient

from app.main import app
from app.tests.conftest import default_user_email, default_user_id


@pytest.mark.asyncio
async def test_read_current_user(client: AsyncClient, default_user_headers):
    response = await client.get(
        app.url_path_for("user_list"), headers=default_user_headers
    )
    assert response.status_code == 200
    assert response.json() == [
        {"email": default_user_email, "full_name": None, "id": default_user_id}
    ]
