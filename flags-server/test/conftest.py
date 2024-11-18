import subprocess
import time
import logging

from typing import Any
from bson import ObjectId

import pytest

from flask import Flask
from flask.testing import FlaskClient

from src.app import app as api_app
from src.app import init
from src.models.Encrypt import Encrypt
from src.models.Flag import Flag
from src.models.Mode import Mode
from src.models.User import User
from src.models.FlagManager import FlagManager
from src.models.ModeManager import ModeManager
from src.models.UserManager import UserManager
from src.data_access.flags_repository import FlagRepository
from src.data_access.modes_repository import ModeRepository
from src.data_access.users_repository import UserRepository

from test.constants import FLAG_MOCK
from test.constants import MODE_MOCK
from test.constants import USER_MOCK
from test.constants import ENCRYPT_MOCK


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
def flag_repository(flask_app: Flask) -> FlagRepository:
    return FlagRepository(db=flask_app.mongo.db)


@pytest.fixture(scope="session")
def mode_repository(flask_app: Flask) -> ModeRepository:
    return ModeRepository(db=flask_app.mongo.db)


@pytest.fixture(scope="session")
def user_repository(flask_app: Flask) -> UserRepository:
    return UserRepository(db=flask_app.mongo.db)


# CLASS
@pytest.fixture(scope="session")
def flag_model() -> Flag:
    TEST_FLAG_MOCK_COPY = FLAG_MOCK['flag'].copy()
    TEST_FLAG_MOCK_COPY["_id"] = ObjectId(TEST_FLAG_MOCK_COPY["_id"])
    return Flag(**TEST_FLAG_MOCK_COPY)


@pytest.fixture(scope="session")
def not_valid_flag_model() -> Flag:
    return Flag(_id=ObjectId(FLAG_MOCK['flag'].get("_id")), name="", image=FLAG_MOCK['flag'].get("image"))


@pytest.fixture(scope="session")
def mode_model() -> Mode:
    TEST_MODE_MOCK_COPY = MODE_MOCK['mode'].copy()
    TEST_MODE_MOCK_COPY["_id"] = ObjectId(TEST_MODE_MOCK_COPY["_id"])
    return Mode(**TEST_MODE_MOCK_COPY)


@pytest.fixture(scope="session")
def user_model() -> User:
    TEST_USER_MOCK_COPY = USER_MOCK['user'].copy()
    TEST_USER_MOCK_COPY["_id"] = ObjectId(TEST_USER_MOCK_COPY["_id"])
    return User(**TEST_USER_MOCK_COPY)


@pytest.fixture(scope="session")
def encrypt_model() -> Encrypt:
    return Encrypt(password=ENCRYPT_MOCK['password'])


@pytest.fixture(scope="session")
def flag_manager_model() -> FlagManager:
    return FlagManager()


@pytest.fixture(scope="session")
def mode_manager_model() -> ModeManager:
    return ModeManager()


@pytest.fixture(scope="session")
def user_manager_model() -> UserManager:
    return UserManager()


# MOCKS CONSTANTS
@pytest.fixture(scope="session")
def test_flag() -> dict[str, str]:
    TEST_FLAG_COPY = FLAG_MOCK['flag'].copy()
    del TEST_FLAG_COPY["_id"]
    return TEST_FLAG_COPY


@pytest.fixture(scope="session")
def test_mode() -> dict[str, str]:
    TEST_MODE_COPY = MODE_MOCK['mode'].copy()
    del TEST_MODE_COPY["_id"]
    return TEST_MODE_COPY


@pytest.fixture(scope="session")
def test_user() -> dict[str, str]:
    TEST_USER_COPY = USER_MOCK['user'].copy()
    del TEST_USER_COPY["_id"]
    return TEST_USER_COPY

@pytest.fixture(scope="session")
def test_user_request() -> dict[str, str]:
    return USER_MOCK['user_request']

@pytest.fixture(scope="session")
def test_flags() -> dict[str, str]:
    return FLAG_MOCK['flags']


@pytest.fixture(scope="session")
def test_modes() -> dict[str, Any]:
    return MODE_MOCK['modes']


@pytest.fixture(scope="session")
def test_users() -> dict[str, Any]:
    return USER_MOCK['users']
