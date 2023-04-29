from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get(app.url_path_for("health_check"))

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}
