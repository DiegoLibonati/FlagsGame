from typing import Any

from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from src.constants.codes import (
    CODE_ERROR_DATABASE,
    CODE_ERROR_GENERIC,
    CODE_ERROR_PYDANTIC,
)
from src.constants.messages import (
    MESSAGE_ERROR_DATABASE,
    MESSAGE_ERROR_GENERIC,
    MESSAGE_ERROR_PYDANTIC,
)


def test_handle_exceptions_base_api_error(error_app: FlaskClient) -> None:
    res: TestResponse = error_app.get("/base-api-error")
    body: dict[str, Any] = res.get_json()

    assert res.status_code == 400
    assert body["code"] == "ERROR_INTERNAL_SERVER"
    assert body["message"] == "Custom API error"


def test_handle_exceptions_pydantic_error(error_app: FlaskClient) -> None:
    res: TestResponse = error_app.get("/pydantic-error")
    body: dict[str, Any] = res.get_json()

    assert res.status_code == 400
    assert body["code"] == CODE_ERROR_PYDANTIC
    assert body["message"] == MESSAGE_ERROR_PYDANTIC
    assert "details" in body["payload"]


def test_handle_exceptions_mongo_error(error_app: FlaskClient) -> None:
    res: TestResponse = error_app.get("/mongo-error")
    body: dict[str, Any] = res.get_json()

    assert res.status_code == 500
    assert body["code"] == CODE_ERROR_DATABASE
    assert body["message"] == MESSAGE_ERROR_DATABASE


def test_handle_exceptions_generic_error(error_app: FlaskClient) -> None:
    res: TestResponse = error_app.get("/generic-error")
    body: dict[str, Any] = res.get_json()

    assert res.status_code == 500
    assert body["code"] == CODE_ERROR_GENERIC
    assert MESSAGE_ERROR_GENERIC.split("{")[0] in body["message"]


def test_handle_exceptions_no_error(error_app: FlaskClient) -> None:
    res: TestResponse = error_app.get("/no-error")
    body: dict[str, Any] = res.get_json()

    assert res.status_code == 200
    assert body["ok"] is True
