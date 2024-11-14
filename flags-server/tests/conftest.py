import subprocess
import time

import pytest

from flask import Flask
from flask import Response
from flask.testing import FlaskClient

from src.app import app as api_app
from src.app import init


prefix_flags_bp = "/v1/flags"
prefix_modes_bp = "/v1/modes"
prefix_users_bp = "/v1/users"

test_flag_mock = {
    "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVnagHgbpRUO82-sIOEi3TX1N3wUGSlRWKZQ&s",
    "name": "test_flag"
}
test_mode_name_mock = "Normal"


@pytest.fixture(scope="session")
def flask_app() -> Flask:
    app = api_app
    init()
    return app


@pytest.fixture(scope="session")
def flask_client(flask_app: Flask) -> FlaskClient:
    return flask_app.test_client()


@pytest.fixture(scope="session")
def mongo_test_db() -> None:
    subprocess.run(
        ["docker-compose", "up", "-d", "flags-db"],
        capture_output=True,
        text=True,
    )

    time.sleep(5)

    yield

    subprocess.run(
        ["docker-compose", "down"],
        capture_output=True,
        text=True,
    )


@pytest.fixture(scope="session")
def flags() -> list[dict[str, str]]:
    return [
        {
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVnagHgbpRUO82-sIOEi3TX1N3wUGSlRWKZQ&s",
            "name": "Argentina"
        },
        {
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Flag_of_Brazil.svg/1200px-Flag_of_Brazil.svg.png",
            "name": "Brasil"
        },
        {
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQt5fAr3G2SRs1TaR3jSiGhYPOdxu4mj8sBtg&s",
            "name": "Peru"
        },
        {
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTyiYirHiGCymBqqOjCzm5A71AuealRFxjiUA&s",
            "name": "Canada"
        },
        {
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS-bu9g_Be9LrSEFgXHGT0jX11SCVgzZNaOfA&s",
            "name": "Estados Unidos"
        },
        {
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQilbazSxXoEzGPXF0J5Oy3FzGUAgxuMu7upg&s",
            "name": "Colombia"
        }
    ]


@pytest.fixture(scope="session")
def test_flag() -> dict[str, str]:
    return test_flag_mock


@pytest.fixture(scope="session")
def inserted_flag_id(flask_client: Flask, test_flag: dict[str, str]) -> str:
    """Fixture to insert a flag and return its ID."""
    response: Response = flask_client.post(
        f"{prefix_flags_bp}/newflag",
        json=test_flag,
    )
    result = response.json
    flag = result.get("fields")
    return flag.get("_id")