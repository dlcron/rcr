import pytest
from fastapi.testclient import TestClient

from rcr.api import app
from rcr.storage import storage


@pytest.fixture(autouse=True)
def clear_storage() -> None:
    storage.clear()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_commands__valid(client: TestClient) -> None:
    response = client.post(
        "/commands",
        json={"commands": ["A", "A", "C"]},
    )
    assert "A" in storage
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}


def test_commands__fetch_result(client: TestClient) -> None:
    storage["A"] = 1
    response = client.get("/rcr/A")
    assert response.status_code == 200


def test_commands__fetch_result_404(client: TestClient) -> None:
    response = client.get("/rcr/B")
    assert response.status_code == 404
