from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)


def test_homepage_returns_200():
    response = client.get("/")
    assert response.status_code == 200


def test_homepage_returns_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_homepage_with_limit_query():
    response = client.get("/?limit=2")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_homepage_invalid_limit():
    response = client.get("/?limit=0")
    assert response.status_code == 422