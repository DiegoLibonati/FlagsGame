import subprocess
import time
import logging

from bson import ObjectId

import pytest

from flask import Flask
from flask import Response
from flask.testing import FlaskClient

from src.app import app as api_app
from src.app import init
from src.models.Flag import Flag
from src.models.Mode import Mode
from src.models.FlagManager import FlagManager
from src.data_access.flags_repository import FlagRepository
from src.data_access.modes_repository import ModeRepository


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# BLUEPRINTS
PREFIX_FLAGS_BP = "/v1/flags"
PREFIX_MODES_BP = "/v1/modes"
PREFIX_USERS_BP = "/v1/users"

# MOCK FLAGS
TEST_FLAG_MOCK = {
    "_id": "673773206d0e53d0d63f3341",
    "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVnagHgbpRUO82-sIOEi3TX1N3wUGSlRWKZQ&s",
    "name": "test_flag"
}
TEST_FLAGS_MOCK = [
    {
        "_id": "67267fd72e10fe5f0af5d706",
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVnagHgbpRUO82-sIOEi3TX1N3wUGSlRWKZQ&s",
        "name": "Argentina"
    },
    {
        "_id": "672680152e10fe5f0af5d707",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Flag_of_Brazil.svg/1200px-Flag_of_Brazil.svg.png",
        "name": "Brasil"
    },
    {
        "_id": "6726819e0291c4ae90b6798c",
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQt5fAr3G2SRs1TaR3jSiGhYPOdxu4mj8sBtg&s",
        "name": "Peru"
    },
    {
        "_id": "672681ac0291c4ae90b6798d",
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTyiYirHiGCymBqqOjCzm5A71AuealRFxjiUA&s",
        "name": "Canada"
    },
    {
        "_id": "672681bf0291c4ae90b6798e",
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS-bu9g_Be9LrSEFgXHGT0jX11SCVgzZNaOfA&s",
        "name": "Estados Unidos"
    },
    {
        "_id": "6728cc43d19b644f5bc6e495",
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQilbazSxXoEzGPXF0J5Oy3FzGUAgxuMu7upg&s",
        "name": "Colombia"
    },
    {
        "_id": "6738a4c6ca44bc6236c37cc4",
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVnagHgbpRUO82-sIOEi3TX1N3wUGSlRWKZQ&s",
        "name": "test_flag"
    }
]
NOT_FOUND_ID_FLAG = "673773206d0e53d0d63f3341"
WRONG_ID_FLAG = "asd"

# MOCK MODES
TEST_MODE_NAME_MOCK = "Normal"
TEST_MODE_MOCK = {
    "_id": "673773206d0e53d0d63f3342",
    "description": "You must guess the most available flags in 10023 seconds.",
    "multiplier": 1000,
    "name": "Test",
    "timeleft": 2500
}
NOT_FOUND_ID_MODE = "673773206d0e53d0d63f3342"
WRONG_ID_MODE = "asd"


# FLAKS FIXTURES
@pytest.fixture(scope="session")
def flask_app() -> Flask:
    app = api_app
    init()
    return app


@pytest.fixture(scope="session")
def flask_client(flask_app: Flask) -> FlaskClient:
    return flask_app.test_client()


@pytest.fixture
def app_context(flask_app) -> None:
    with flask_app.app_context():
        yield


# MONGO FIXTURES
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


# REPOSITORIES - SERVICES
@pytest.fixture(scope="session")
def flag_repository() -> FlagRepository:
    return FlagRepository()


@pytest.fixture(scope="session")
def mode_repository() -> ModeRepository:
    return ModeRepository()


# CLASS
@pytest.fixture(scope="session")
def flag_model() -> Flag:
    TEST_FLAG_MOCK_COPY = TEST_FLAG_MOCK.copy()
    TEST_FLAG_MOCK_COPY["_id"] = ObjectId(TEST_FLAG_MOCK_COPY["_id"])
    return Flag(**TEST_FLAG_MOCK_COPY)


@pytest.fixture(scope="session")
def not_valid_flag_model() -> Flag:
    return Flag(_id=ObjectId(TEST_FLAG_MOCK.get("_id")), name="", image=TEST_FLAG_MOCK.get("image"))


@pytest.fixture(scope="session")
def mode_model() -> Mode:
    TEST_MODE_MOCK_COPY = TEST_MODE_MOCK.copy()
    TEST_MODE_MOCK_COPY["_id"] = ObjectId(TEST_MODE_MOCK_COPY["_id"])
    return Mode(**TEST_MODE_MOCK_COPY)


@pytest.fixture(scope="session")
def flag_manager_model() -> FlagManager:
    return FlagManager()


# MOCKS CONSTANTS
@pytest.fixture(scope="session")
def test_flag() -> dict[str, str]:
    TEST_FLAG_COPY = TEST_FLAG_MOCK.copy()
    del TEST_FLAG_COPY["_id"]
    return TEST_FLAG_COPY


@pytest.fixture(scope="session")
def test_mode() -> dict[str, str]:
    TEST_MODE_COPY = TEST_MODE_MOCK.copy()
    del TEST_MODE_COPY["_id"]
    return TEST_MODE_COPY


@pytest.fixture(scope="session")
def test_flags() -> dict[str, str]:
    return TEST_FLAGS_MOCK


# SAVE DOCS MONGO
@pytest.fixture(scope="function")
def inserted_flag_id(flask_client: Flask, test_flag: dict[str, str]) -> str:
    """Fixture to insert a flag and return its ID."""
    response: Response = flask_client.post(
        f"{PREFIX_FLAGS_BP}/newflag",
        json=test_flag,
    )
    result = response.json
    flag = result.get("data")
    return flag.get("_id")


# @pytest.fixture(scope="session")
# def modes() -> dict[str, Any]:
#     return [
#         {
#             "_id": "672687090bcd13f7c9a88ac3",
#             "description": "You must guess the most available flags in 90 seconds.",
#             "multiplier": 10,
#             "name": "Normal",
#             "timeleft": 90
#         },
#         {
#             "_id": "6726874dde5266d8ba53ae77",
#             "description": "You must guess the most available flags in 60 seconds.",
#             "multiplier": 25,
#             "name": "Hard",
#             "timeleft": 60
#         },
#         {
#             "_id": "67268757de5266d8ba53ae78",
#             "description": "You must guess the most available flags in 25 seconds.",
#             "multiplier": 100,
#             "name": "Hardcore",
#             "timeleft": 25
#         }
#     ]


# @pytest.fixture(scope="session")
# def test_mode() -> dict[str, Any]:
#     return test_mode_mock


# @pytest.fixture(scope="session")
# def inserted_mode_id(flask_client: Flask, test_mode: dict[str, Any]) -> str:
#     """Fixture to insert a mode and return its ID."""
#     response: Response = flask_client.post(
#         f"{prefix_modes_bp}/newmode",
#         json=test_mode,
#     )
#     result = response.json
#     mode = result.get("fields")
#     return mode.get("_id")