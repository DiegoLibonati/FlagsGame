import subprocess
import time
import uuid
from test.constants import COMPOSE_FILE
from typing import Any

import pytest
from flask import Blueprint, Flask, Response, jsonify
from flask.testing import FlaskClient
from pydantic import BaseModel
from pymongo.errors import PyMongoError

from app import create_app
from src.services.flag_service import FlagService
from src.services.mode_service import ModeService
from src.services.user_service import UserService
from src.utils.error_handler import handle_exceptions
from src.utils.exceptions import ValidationAPIError


@pytest.fixture(scope="session")
def flask_app(mongo_test_db: None) -> Flask:
    app = create_app()
    return app


@pytest.fixture(scope="session")
def flask_client(flask_app: Flask) -> FlaskClient:
    return flask_app.test_client()


@pytest.fixture
def error_app() -> FlaskClient:
    app = Flask(__name__)
    bp = Blueprint("test_errors", __name__)

    @bp.route("/base-api-error")
    @handle_exceptions
    def raise_base_api_error() -> None:
        raise ValidationAPIError(message="Custom API error")

    @bp.route("/pydantic-error")
    @handle_exceptions
    def raise_pydantic_error() -> Response:
        class Model(BaseModel):
            x: int

        Model(x="not-an-int")
        return jsonify({"ok": True})

    @bp.route("/mongo-error")
    @handle_exceptions
    def raise_mongo_error() -> None:
        raise PyMongoError("Mongo failed")

    @bp.route("/generic-error")
    @handle_exceptions
    def raise_generic_error() -> None:
        raise RuntimeError("Unexpected failure")

    @bp.route("/no-error")
    @handle_exceptions
    def no_error() -> Response:
        return jsonify({"ok": True})

    app.register_blueprint(bp)
    return app.test_client()


@pytest.fixture(scope="session")
def mongo_test_db() -> None:
    subprocess.run(
        ["docker-compose", "-f", COMPOSE_FILE, "up", "-d", "flags-db"],
        check=True,
    )

    time.sleep(5)

    yield

    subprocess.run(
        ["docker-compose", "-f", COMPOSE_FILE, "down"],
        check=True,
    )


@pytest.fixture
def unique_flag() -> dict[str, Any]:
    return {
        "name": f"test_flag_{uuid.uuid4().hex[:6]}",
        "image": "https://test.com/img.png",
    }


@pytest.fixture
def unique_mode() -> dict[str, Any]:
    return {
        "name": f"test_mode_{uuid.uuid4().hex[:6]}",
        "description": "Mode used for testing",
        "multiplier": 25,
        "timeleft": 90,
    }


@pytest.fixture
def unique_user() -> dict[str, Any]:
    return {
        "username": f"test_user_{uuid.uuid4().hex[:6]}",
        "password": "hi1234",
        "score": 250,
    }


@pytest.fixture(autouse=True)
def clean_flags():
    for flag in FlagService.get_all_flags():
        FlagService.delete_flag_by_id(flag["_id"])
    yield


@pytest.fixture(autouse=True)
def clean_modes():
    for mode in ModeService.get_all_modes():
        ModeService.delete_mode_by_id(mode["_id"])
    yield


@pytest.fixture(autouse=True)
def clean_users():
    for user in UserService.get_all_users():
        UserService.delete_user_by_id(user["_id"])
    yield
