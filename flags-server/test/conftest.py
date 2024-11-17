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
from src.models.Encrypt import Encrypt
from src.models.Flag import Flag
from src.models.Mode import Mode
from src.models.User import User
from src.models.FlagManager import FlagManager
from src.data_access.flags_repository import FlagRepository
from src.data_access.modes_repository import ModeRepository
from src.data_access.users_repository import UserRepository

from test.constants import TEST_FLAG_MOCK
from test.constants import TEST_FLAGS_MOCK
from test.constants import TEST_MODE_MOCK
from test.constants import TEST_USER_MOCK
from test.constants import PREFIX_FLAGS_BP
from test.constants import PASSWORD


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


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


@pytest.fixture(scope="session")
def user_repository() -> UserRepository:
    return UserRepository()


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
def user_model() -> User:
    TEST_USER_MOCK_COPY = TEST_USER_MOCK.copy()
    TEST_USER_MOCK_COPY["_id"] = ObjectId(TEST_USER_MOCK_COPY["_id"])
    return User(**TEST_USER_MOCK_COPY)


@pytest.fixture(scope="session")
def encrypt_model() -> Encrypt:
    return Encrypt(password=PASSWORD)


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
def test_user() -> dict[str, str]:
    TEST_USER_COPY = TEST_USER_MOCK.copy()
    del TEST_USER_COPY["_id"]
    return TEST_USER_COPY


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