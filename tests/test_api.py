import pytest
from fastapi.testclient import TestClient

from rcr.api import app
from rcr.config import Settings
from rcr.storage import storage


@pytest.fixture(autouse=True)
def clear_storage() -> None:
    storage.clear()


@pytest.fixture
def commands(monkeypatch, tmp_path) -> None:
    settings = Settings()
    settings.commands = ["A", "B", "C"]

    monkeypatch.setattr("rcr.api.models.settings", settings)


@pytest.fixture
def client(commands: None) -> TestClient:
    return TestClient(app)


def test_commands__valid(client: TestClient) -> None:
    response = client.post(
        "/commands",
        json={"commands": ["A", "A", "C"]},
    )
    assert "A" in storage
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}


def test_commands__invalid(client: TestClient) -> None:
    response = client.post(
        "/commands",
        json={"commands": ["A", "D"]},
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "commands", 1],
                "msg": "Unknown command 'D'.",
                "type": "value_error",
            }
        ]
    }


def test_commands__fetch_result(client: TestClient) -> None:
    storage["A"] = 1
    response = client.get("/rcr/A")
    assert response.status_code == 200


def test_commands__fetch_result_404(client: TestClient) -> None:
    response = client.get("/rcr/B")
    assert response.status_code == 404
