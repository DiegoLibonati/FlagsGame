from test.constants import BLUEPRINTS
from typing import Any

from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from src.constants.codes import (
    CODE_ERROR_AUTHENTICATION,
    CODE_NOT_FOUND_MODE,
    CODE_NOT_FOUND_USER,
    CODE_SUCCESS_ADD_USER,
    CODE_SUCCESS_DELETE_USER,
    CODE_SUCCESS_GET_GLOBAL_TOP_USER,
    CODE_SUCCESS_UPDATE_USER,
)
from src.constants.messages import (
    MESSAGE_ERROR_AUTHENTICATION,
    MESSAGE_NOT_FOUND_MODE,
    MESSAGE_NOT_FOUND_USER,
    MESSAGE_SUCCESS_ADD_USER,
    MESSAGE_SUCCESS_DELETE_USER,
    MESSAGE_SUCCESS_GET_GLOBAL_TOP_USER,
    MESSAGE_SUCCESS_UPDATE_USER,
)


def test_alive(flask_client: FlaskClient) -> None:
    res: TestResponse = flask_client.get(f"{BLUEPRINTS['users']}/alive")
    body: dict[str, Any] = res.get_json()

    assert res.status_code == 200
    assert body["name_bp"] == "Users"
    assert body["message"] == "I am Alive!"


def test_top_general(flask_client: FlaskClient) -> None:
    res: TestResponse = flask_client.get(f"{BLUEPRINTS['users']}/top_global")
    body: dict[str, Any] = res.get_json()

    assert res.status_code == 200
    assert body["code"] == CODE_SUCCESS_GET_GLOBAL_TOP_USER
    assert body["message"] == MESSAGE_SUCCESS_GET_GLOBAL_TOP_USER
    assert isinstance(body["data"], list)


def test_add_user_success(
    flask_client: FlaskClient, unique_mode: dict[str, Any], unique_user: dict[str, Any]
) -> None:
    res_mode: TestResponse = flask_client.post(
        f"{BLUEPRINTS['modes']}/", json=unique_mode
    )
    mode_id: str = res_mode.get_json()["data"]["_id"]

    user_data: dict[str, Any] = {
        **unique_user,
        "mode_id": mode_id,
    }

    res: TestResponse = flask_client.post(f"{BLUEPRINTS['users']}/", json=user_data)
    body: dict[str, Any] = res.get_json()

    assert res.status_code == 201
    assert body["code"] == CODE_SUCCESS_ADD_USER
    assert body["message"] == MESSAGE_SUCCESS_ADD_USER
    assert body["data"]["username"] == user_data["username"]
    assert "password" not in body["data"]
    assert "_id" in body["data"]


def test_add_user_mode_not_found(
    flask_client: FlaskClient, unique_user: dict[str, Any]
) -> None:
    user_data: dict[str, Any] = {
        **unique_user,
        "mode_id": "673773206d0e53d0d63f3343",
    }

    res: TestResponse = flask_client.post(f"{BLUEPRINTS['users']}/", json=user_data)
    body: dict[str, Any] = res.get_json()

    assert res.status_code == 404
    assert body["code"] == CODE_NOT_FOUND_MODE
    assert body["message"] == MESSAGE_NOT_FOUND_MODE


def test_modify_user_success(
    flask_client: FlaskClient, unique_mode: dict[str, Any], unique_user: dict[str, Any]
) -> None:
    res_mode: TestResponse = flask_client.post(
        f"{BLUEPRINTS['modes']}/", json=unique_mode
    )
    mode_id: str = res_mode.get_json()["data"]["_id"]

    user_data: dict[str, Any] = {
        **unique_user,
        "mode_id": mode_id,
    }

    flask_client.post(f"{BLUEPRINTS['users']}/", json=user_data)

    modify_data: dict[str, Any] = {
        **unique_user,
        "score": 75,
        "mode_id": mode_id,
    }

    res: TestResponse = flask_client.patch(f"{BLUEPRINTS['users']}/", json=modify_data)
    body: dict[str, Any] = res.get_json()

    assert res.status_code == 200
    assert body["code"] == CODE_SUCCESS_UPDATE_USER
    assert body["message"] == MESSAGE_SUCCESS_UPDATE_USER
    assert body["data"]["scores"][unique_mode["name"]] == 75


def test_modify_user_mode_not_found(
    flask_client: FlaskClient, unique_user: dict[str, Any]
) -> None:
    modify_data: dict[str, Any] = {
        **unique_user,
        "mode_id": "673773206d0e53d0d63f3343",
    }

    res: TestResponse = flask_client.patch(f"{BLUEPRINTS['users']}/", json=modify_data)
    body: dict[str, Any] = res.get_json()

    assert res.status_code == 404
    assert body["code"] == CODE_NOT_FOUND_MODE
    assert body["message"] == MESSAGE_NOT_FOUND_MODE


def test_modify_user_not_found(
    flask_client: FlaskClient, unique_mode: dict[str, Any], unique_user: dict[str, Any]
) -> None:
    res_mode: TestResponse = flask_client.post(
        f"{BLUEPRINTS['modes']}/", json=unique_mode
    )
    mode_id: str = res_mode.get_json()["data"]["_id"]

    modify_data: dict[str, Any] = {
        **unique_user,
        "username": "non_existing",
        "mode_id": mode_id,
    }

    res: TestResponse = flask_client.patch(f"{BLUEPRINTS['users']}/", json=modify_data)
    body: dict[str, Any] = res.get_json()

    assert res.status_code == 404
    assert body["code"] == CODE_NOT_FOUND_USER
    assert body["message"] == MESSAGE_NOT_FOUND_USER


def test_modify_user_authentication_error(
    flask_client: FlaskClient, unique_mode: dict[str, Any], unique_user: dict[str, Any]
) -> None:
    res_mode: TestResponse = flask_client.post(
        f"{BLUEPRINTS['modes']}/", json=unique_mode
    )
    mode_id: str = res_mode.get_json()["data"]["_id"]

    user_data: dict[str, Any] = {
        **unique_user,
        "mode_id": mode_id,
    }

    flask_client.post(f"{BLUEPRINTS['users']}/", json=user_data)

    modify_data: dict[str, Any] = {
        **unique_user,
        "password": "wrong",
        "mode_id": mode_id,
    }

    res: TestResponse = flask_client.patch(f"{BLUEPRINTS['users']}/", json=modify_data)
    body: dict[str, Any] = res.get_json()

    assert res.status_code == 401
    assert body["code"] == CODE_ERROR_AUTHENTICATION
    assert body["message"] == MESSAGE_ERROR_AUTHENTICATION


def test_delete_user_success(
    flask_client: FlaskClient, unique_mode: dict[str, Any], unique_user: dict[str, Any]
) -> None:
    res_mode: TestResponse = flask_client.post(
        f"{BLUEPRINTS['modes']}/", json=unique_mode
    )
    mode_id: str = res_mode.get_json()["data"]["_id"]

    user_data: dict[str, Any] = {
        **unique_user,
        "mode_id": mode_id,
    }

    res_insert: TestResponse = flask_client.post(
        f"{BLUEPRINTS['users']}/", json=user_data
    )
    _id: str = res_insert.get_json()["data"]["_id"]

    res: TestResponse = flask_client.delete(f"{BLUEPRINTS['users']}/{_id}")
    body: dict[str, Any] = res.get_json()

    assert res.status_code == 200
    assert body["code"] == CODE_SUCCESS_DELETE_USER
    assert body["message"] == MESSAGE_SUCCESS_DELETE_USER


def test_delete_user_not_found(flask_client: FlaskClient) -> None:
    res: TestResponse = flask_client.delete(
        f"{BLUEPRINTS['users']}/673773206d0e53d0d63f3343"
    )
    body: dict[str, Any] = res.get_json()

    assert res.status_code == 404
    assert body["code"] == CODE_NOT_FOUND_USER
    assert body["message"] == MESSAGE_NOT_FOUND_USER
