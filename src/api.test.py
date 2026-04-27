import os
import socket
import subprocess
import sys
import time
from pathlib import Path
from typing import Generator

import httpx
import pytest


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


@pytest.fixture
def api_url(tmp_path: Path) -> Generator[str, None, None]:
    port = find_free_port()
    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_ROOT)

    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "src.server:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
        ],
        cwd=tmp_path,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    base_url = f"http://127.0.0.1:{port}/api/todos"
    deadline = time.time() + 10

    with httpx.Client() as client:
        while time.time() < deadline:
            try:
                response = client.get(base_url)
                if response.status_code == 200:
                    break
            except httpx.HTTPError:
                pass
            time.sleep(0.1)
        else:
            process.terminate()
            process.wait(timeout=5)
            pytest.fail("API server did not start in time")

    yield base_url

    process.terminate()
    process.wait(timeout=5)


@pytest.fixture
def target_id(api_url: str) -> int:
    with httpx.Client() as client:
        response = client.post(api_url, json={"title": "テストタスク"})

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "テストタスク"
    assert data["done"] is False

    return int(data["id"])


def test_post_creates_todo(api_url: str) -> None:
    with httpx.Client() as client:
        response = client.post(api_url, json={"title": "テストタスク"})

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "テストタスク"
    assert data["done"] is False


def test_get_returns_added_todo(api_url: str, target_id: int) -> None:
    with httpx.Client() as client:
        response = client.get(api_url)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    found = next((todo for todo in data if todo["id"] == target_id), None)
    assert found is not None


def test_put_updates_todo_to_done(api_url: str, target_id: int) -> None:
    with httpx.Client() as client:
        response = client.put(f"{api_url}/{target_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["done"] is True


def test_delete_removes_todo(api_url: str, target_id: int) -> None:
    with httpx.Client() as client:
        response = client.delete(f"{api_url}/{target_id}")

    assert response.status_code == 200


def test_validation_rejects_blank_title(api_url: str) -> None:
    with httpx.Client() as client:
        response = client.post(api_url, json={"title": "   "})

    assert response.status_code == 400
    data = response.json()
    assert data["error"] == "タイトルは必須です"
