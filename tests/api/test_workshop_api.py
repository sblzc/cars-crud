"""Section 4 of the testing workshop: HTTP tests driven through TestClient."""

import pytest

pytestmark = pytest.mark.api


def test_post_car_returns_201_and_json(client, car_payload):
    response = client.post("/api/cars", json=car_payload)
    assert response.status_code == 201
    assert response.headers["content-type"] == "application/json"
    created = response.json()
    assert created["id"] > 0
    assert created["make"] == car_payload["make"]
    assert created["model"] == car_payload["model"]
    assert created["year"] == car_payload["year"]
    assert created["color"] == car_payload["color"]


def test_invalid_year_is_not_saved(client):
    invalid = {"make": "Toyota", "model": "Corolla", "year": 1800}

    response = client.post("/api/cars", json=invalid)

    assert response.status_code == 422
    assert client.get("/api/cars").json() == []
