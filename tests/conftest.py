from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


def pytest_addoption(parser):
    # Registered here rather than in tests/e2e/conftest.py: pytest parses the
    # command line before it collects anything, and only preloads the conftest
    # files of paths named on that command line. Running the whole suite
    # (`pytest`, which uses testpaths = tests) never names tests/e2e, so an
    # option registered there would not exist and the e2e fixture's
    # pytestconfig.getoption("--headed") would raise
    # "ValueError: no option named 'headed'".
    parser.addoption("--headed", action="store_true", help="Show the E2E browser window")


@pytest.fixture
def database_path(tmp_path: Path) -> Path:
    return tmp_path / "test-cars.db"


@pytest.fixture
def client(database_path: Path) -> Iterator[TestClient]:
    # The context manager runs FastAPI's lifespan, including table creation.
    # Each test gets a fresh on-disk database, never the real cars.db.
    with TestClient(create_app(database_path)) as test_client:
        yield test_client


@pytest.fixture
def car_payload() -> dict:
    return {"make": "Toyota", "model": "Corolla", "year": 2024, "color": "Silver"}
