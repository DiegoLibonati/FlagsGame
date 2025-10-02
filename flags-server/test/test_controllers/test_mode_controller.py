from test.constants import BLUEPRINTS
from typing import Any

from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from src.constants.codes import (
    CODE_NOT_FOUND_MODE,
    CODE_SUCCESS_ADD_MODE,
    CODE_SUCCESS_DELETE_MODE,
    CODE_SUCCESS_GET_ALL_MODES,
    CODE_SUCCESS_GET_MODE,
    CODE_SUCCESS_GET_TOP_MODE,
)
from src.constants.messages import (
    MESSAGE_NOT_FOUND_MODE,
    MESSAGE_SUCCESS_ADD_MODE,
    MESSAGE_SUCCESS_DELETE_MODE,
    MESSAGE_SUCCESS_GET_ALL_MODES,
    MESSAGE_SUCCESS_GET_MODE,
    MESSAGE_SUCCESS_GET_TOP_MODE,
)


def test_alive(flask_client: FlaskClient) -> None:
    res: TestResponse = flask_client.get(f"{BLUEPRINTS['modes']}/alive")
    body: dict[str, Any] = res.get_json()

    assert res.status_code == 200
    assert body["name_bp"] == "Modes"
    assert body["message"] == "I am Alive!"


def test_get_modes_initially_empty(flask_client: FlaskClient) -> None:
    res: TestResponse = flask_client.get(f"{BLUEPRINTS['modes']}/")
    body: dict[str, Any] = res.get_json()

    assert res.status_code == 200
    assert body["code"] == CODE_SUCCESS_GET_ALL_MODES
    assert body["message"] == MESSAGE_SUCCESS_GET_ALL_MODES
    assert isinstance(body["data"], list)


def test_add_mode_success(
    flask_client: FlaskClient, unique_mode: dict[str, Any]
) -> None:
    res: TestResponse = flask_client.post(f"{BLUEPRINTS['modes']}/", json=unique_mode)
    body: dict[str, Any] = res.get_json()

    assert res.status_code == 201
    assert body["code"] == CODE_SUCCESS_ADD_MODE
    assert body["message"] == MESSAGE_SUCCESS_ADD_MODE
    assert body["data"]["name"] == unique_mode["name"]
    assert "_id" in body["data"]


def test_add_mode_conflict(
    flask_client: FlaskClient, unique_mode: dict[str, Any]
) -> None:
    flask_client.post(f"{BLUEPRINTS['modes']}/", json=unique_mode)
    res: TestResponse = flask_client.post(f"{BLUEPRINTS['modes']}/", json=unique_mode)

    assert res.status_code == 409


def test_find_mode_success(
    flask_client: FlaskClient, unique_mode: dict[str, Any]
) -> None:
    res_insert: TestResponse = flask_client.post(
        f"{BLUEPRINTS['modes']}/", json=unique_mode
    )
    _id: str = res_insert.get_json()["data"]["_id"]

    res: TestResponse = flask_client.get(f"{BLUEPRINTS['modes']}/{_id}")
    body: dict[str, Any] = res.get_json()

    assert res.status_code == 200
    assert body["code"] == CODE_SUCCESS_GET_MODE
    assert body["message"] == MESSAGE_SUCCESS_GET_MODE
    assert body["data"]["name"] == unique_mode["name"]


def test_find_mode_not_found(flask_client: FlaskClient) -> None:
    res: TestResponse = flask_client.get(
        f"{BLUEPRINTS['modes']}/673773206d0e53d0d63f3343"
    )
    body: dict[str, Any] = res.get_json()

    assert res.status_code == 404
    assert body["code"] == CODE_NOT_FOUND_MODE
    assert body["message"] == MESSAGE_NOT_FOUND_MODE


def test_top_mode_success(
    flask_client: FlaskClient, unique_mode: dict[str, Any]
) -> None:
    res_insert: TestResponse = flask_client.post(
        f"{BLUEPRINTS['modes']}/", json=unique_mode
    )
    _id: str = res_insert.get_json()["data"]["_id"]

    res: TestResponse = flask_client.get(f"{BLUEPRINTS['modes']}/{_id}/top")
    body: dict[str, Any] = res.get_json()

    assert res.status_code == 200
    assert body["code"] == CODE_SUCCESS_GET_TOP_MODE
    assert body["message"] == MESSAGE_SUCCESS_GET_TOP_MODE
    assert isinstance(body["data"], list)


def test_delete_mode_success(
    flask_client: FlaskClient, unique_mode: dict[str, Any]
) -> None:
    res_insert: TestResponse = flask_client.post(
        f"{BLUEPRINTS['modes']}/", json=unique_mode
    )
    _id: str = res_insert.get_json()["data"]["_id"]

    res: TestResponse = flask_client.delete(f"{BLUEPRINTS['modes']}/{_id}")
    body: dict[str, Any] = res.get_json()

    assert res.status_code == 200
    assert body["code"] == CODE_SUCCESS_DELETE_MODE
    assert body["message"] == MESSAGE_SUCCESS_DELETE_MODE


def test_delete_mode_not_found(flask_client: FlaskClient) -> None:
    res: TestResponse = flask_client.delete(
        f"{BLUEPRINTS['modes']}/673773206d0e53d0d63f3343"
    )
    body: dict[str, Any] = res.get_json()

    assert res.status_code == 404
    assert body["code"] == CODE_NOT_FOUND_MODE
    assert body["message"] == MESSAGE_NOT_FOUND_MODE
