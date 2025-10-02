from test.constants import BLUEPRINTS
from typing import Any

from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from src.constants.codes import (
    CODE_ERROR_VALUE_IS_NOT_INTEGER,
    CODE_NOT_FOUND_FLAG,
    CODE_SUCCESS_ADD_FLAG,
    CODE_SUCCESS_DELETE_FLAG,
    CODE_SUCCESS_GET_ALL_FLAGS,
)
from src.constants.messages import (
    MESSAGE_ERROR_VALUE_IS_NOT_INTEGER,
    MESSAGE_NOT_FOUND_FLAG,
    MESSAGE_SUCCESS_ADD_FLAG,
    MESSAGE_SUCCESS_DELETE_FLAG,
    MESSAGE_SUCCESS_GET_ALL_FLAGS,
)


def test_alive(flask_client: FlaskClient) -> None:
    res: TestResponse = flask_client.get(f"{BLUEPRINTS['flags']}/alive")
    body: dict[str, Any] = res.get_json()

    assert res.status_code == 200
    assert body["name_bp"] == "Flags"
    assert body["message"] == "I am Alive!"


def test_get_flags_initially_empty(flask_client: FlaskClient) -> None:
    res: TestResponse = flask_client.get(f"{BLUEPRINTS['flags']}/")
    body: dict[str, Any] = res.get_json()

    assert res.status_code == 200
    assert body["code"] == CODE_SUCCESS_GET_ALL_FLAGS
    assert body["message"] == MESSAGE_SUCCESS_GET_ALL_FLAGS
    assert isinstance(body["data"], list)


def test_add_flag_success(
    flask_client: FlaskClient, unique_flag: dict[str, Any]
) -> None:
    res: TestResponse = flask_client.post(f"{BLUEPRINTS['flags']}/", json=unique_flag)
    body: dict[str, Any] = res.get_json()

    assert res.status_code == 201
    assert body["code"] == CODE_SUCCESS_ADD_FLAG
    assert body["message"] == MESSAGE_SUCCESS_ADD_FLAG
    assert body["data"]["name"] == unique_flag["name"]
    assert "_id" in body["data"]


def test_add_flag_conflict(
    flask_client: FlaskClient, unique_flag: dict[str, Any]
) -> None:
    flask_client.post(f"{BLUEPRINTS['flags']}/", json=unique_flag)
    res: TestResponse = flask_client.post(f"{BLUEPRINTS['flags']}/", json=unique_flag)

    assert res.status_code == 409


def test_get_random_flags_invalid_quantity(flask_client: FlaskClient) -> None:
    res: TestResponse = flask_client.get(f"{BLUEPRINTS['flags']}/random/not-a-number")
    body: dict[str, Any] = res.get_json()

    assert res.status_code == 400
    assert body["code"] == CODE_ERROR_VALUE_IS_NOT_INTEGER
    assert body["message"] == MESSAGE_ERROR_VALUE_IS_NOT_INTEGER


def test_get_random_flags_success(
    flask_client: FlaskClient, unique_flag: dict[str, Any]
) -> None:
    flask_client.post(f"{BLUEPRINTS['flags']}/", json=unique_flag)

    res: TestResponse = flask_client.get(f"{BLUEPRINTS['flags']}/random/1")
    body: dict[str, Any] = res.get_json()

    assert res.status_code == 200
    assert body["code"] == CODE_SUCCESS_GET_ALL_FLAGS
    assert body["message"] == MESSAGE_SUCCESS_GET_ALL_FLAGS
    assert isinstance(body["data"], list)
    assert len(body["data"]) == 1


def test_delete_flag_success(
    flask_client: FlaskClient, unique_flag: dict[str, Any]
) -> None:
    res_insert: TestResponse = flask_client.post(
        f"{BLUEPRINTS['flags']}/", json=unique_flag
    )
    _id: str = res_insert.get_json()["data"]["_id"]

    res: TestResponse = flask_client.delete(f"{BLUEPRINTS['flags']}/{_id}")
    body: dict[str, Any] = res.get_json()

    assert res.status_code == 200
    assert body["code"] == CODE_SUCCESS_DELETE_FLAG
    assert body["message"] == MESSAGE_SUCCESS_DELETE_FLAG


def test_delete_flag_not_found(flask_client: FlaskClient) -> None:
    res: TestResponse = flask_client.delete(
        f"{BLUEPRINTS['flags']}/673773206d0e53d0d63f3343"
    )
    body: dict[str, Any] = res.get_json()

    assert res.status_code == 404
    assert body["code"] == CODE_NOT_FOUND_FLAG
    assert body["message"] == MESSAGE_NOT_FOUND_FLAG
