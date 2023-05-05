import pytest
from fastapi import status
from fastapi.testclient import TestClient
from rcr.api import app
from rcr.storage import storage


@pytest.fixture(autouse=True)
def _clear_storage() -> None:
    storage.clear()


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)


def test_commands__valid(client: TestClient) -> None:
    response = client.post(
        "/commands",
        json={"commands": ["A", "A", "C"]},
    )
    assert "A" in storage
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "OK"}


def test_commands__fetch_result(client: TestClient) -> None:
    storage["A"] = 1
    response = client.get("/rcr/A")
    assert response.status_code == status.HTTP_200_OK


def test_commands__fetch_result_404(client: TestClient) -> None:
    response = client.get("/rcr/B")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_happy_path(client: TestClient) -> None:
    response = client.post(
        "/commands",
        json={"commands": ["LEFT"] * 4 + ["GRAB"] * 1 + ["BACK"] * 2},
    )
    assert response.status_code == status.HTTP_200_OK
    for command, value in {"LEFT": "1", "GRAB": "00", "BACK": "01"}.items():
        assert client.get(f"/rcr/{command}").json()["rcr"] == value
