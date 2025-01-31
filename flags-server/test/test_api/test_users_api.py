import pytest

from flask import Flask
from flask import Response

from src.data_access.users_repository import UserRepository

from test.constants import BLUEPRINTS
from test.constants import USER_MOCK


@pytest.mark.usefixtures("mongo_test_db")
def test_add_user(flask_client: Flask, test_user_request: dict[str, str]) -> None:
    username = test_user_request.get("username")
    score = test_user_request.get("score")
    mode_name = test_user_request.get("mode_name")

    response: Response = flask_client.post(
        f"{BLUEPRINTS['users']}/addormodify",
        json=test_user_request
    )

    result = response.json
    status_code = response.status_code

    message = result.get("message")
    data = result.get("data")

    assert status_code == 201
    assert message == "User successfully added."
    assert isinstance(data, dict)
    assert data
    assert data.get("_id")
    assert data.get("username") == username
    assert data["scores"].get(mode_name) == score

@pytest.mark.usefixtures("mongo_test_db")
def test_try_to_add_user_again(flask_client: Flask, test_user_request: dict[str, str]) -> None:
    username = test_user_request.get("username")
    score = 205
    mode_name = test_user_request.get("mode_name")

    response: Response = flask_client.post(
        f"{BLUEPRINTS['users']}/addormodify",
        json=test_user_request
    )

    result = response.json
    status_code = response.status_code

    message = result.get("message")
    data = result.get("data")

    assert status_code == 400
    assert message == "There is a user with that username."
    assert isinstance(data, dict)
    assert data
    assert data.get("_id")
    assert data.get("username") == username
    assert not data["scores"].get(mode_name) == score

@pytest.mark.usefixtures("mongo_test_db")
def test_modify_user(flask_client: Flask, test_user_request: dict[str, str]) -> None:
    username = test_user_request.get("username")
    password = test_user_request.get("password")
    score = USER_MOCK['scores_updated']["hard"]
    mode_name = "hard"

    response: Response = flask_client.put(
        f"{BLUEPRINTS['users']}/addormodify",
        json={
            "username": username,
            "password": password,
            "score": score,
            "mode_name": mode_name
        }
    )

    result = response.json
    status_code = response.status_code

    message = result.get("message")
    data = result.get("data")

    assert status_code == 201
    assert message == "User successfully updated."
    assert isinstance(data, dict)
    assert data
    assert data.get("_id")
    assert data.get("username") == username
    assert data["scores"].get(mode_name) == score

@pytest.mark.usefixtures("mongo_test_db")
def test_try_to_modify_user_without_user(flask_client: Flask, test_user_request: dict[str, str]) -> None:
    username =  USER_MOCK['wrong_user_username']
    password = test_user_request.get("password")
    score = test_user_request.get("score")
    mode_name = test_user_request.get("mode_name")

    response: Response = flask_client.put(
        f"{BLUEPRINTS['users']}/addormodify",
        json={
            "username": username,
            "password": password,
            "score": score,
            "mode_name": mode_name
        }
    )

    result = response.json
    status_code = response.status_code

    message = result.get("message")
    data = result.get("data")

    assert status_code == 404
    assert message == "No valid user was found based on the data entered."
    assert not data

@pytest.mark.usefixtures("mongo_test_db")
def test_try_to_modify_user_with_wrong_password(flask_client: Flask, test_user_request: dict[str, str]) -> None:
    username = test_user_request.get("username")
    password = USER_MOCK['wrong_user_password']
    score = test_user_request.get("score")
    mode_name = test_user_request.get("mode_name")

    response: Response = flask_client.put(
        f"{BLUEPRINTS['users']}/addormodify",
        json={
            "username": username,
            "password": password,
            "score": score,
            "mode_name": mode_name
        }
    )

    result = response.json
    status_code = response.status_code

    message = result.get("message")
    data = result.get("data")

    assert status_code == 400
    assert message == "Password do not match with that username."
    assert not data

@pytest.mark.usefixtures("mongo_test_db")
def test_add_or_modify_user_with_wrong_user(flask_client: Flask) -> None:
    response: Response = flask_client.post(
        f"{BLUEPRINTS['users']}/addormodify",
        json={
            "username": "",
            "password": "1234",
            "score": "200",
            "mode_name": "general"
        }
    )

    result = response.json
    status_code = response.status_code

    message = result.get("message")
    data = result.get("data")

    assert status_code == 400
    assert message == "The data entered are not valid."
    assert not data

@pytest.mark.usefixtures("mongo_test_db")
def test_add_or_modify_user_with_wrong_mode_name(flask_client: Flask) -> None:
    response: Response = flask_client.post(
        f"{BLUEPRINTS['users']}/addormodify",
        json={
            "username": "asd",
            "password": "1234",
            "score": 200,
            "mode_name": USER_MOCK['wrong_user_mode_name']
        }
    )

    result = response.json
    status_code = response.status_code

    message = result.get("message")
    data = result.get("data")

    assert status_code == 404
    assert message == "The mode entered does not exist in the database."
    assert not data

@pytest.mark.usefixtures("mongo_test_db")
def test_get_top_general(flask_client: Flask) -> None:
    response: Response = flask_client.get(
        f"{BLUEPRINTS['users']}/top/general"
    )

    result = response.json
    status_code = response.status_code

    message = result.get("message")
    data = result.get("data")

    assert status_code == 200
    assert message == "Successfully obtained the global top."
    assert isinstance(data, list)

    if len(data) >= 2:
        first_user = data[0]
        second_user = data[1]

        assert first_user.get("score") >= second_user.get("score")

    assert len(data) >= 0 and len(data) <= 10

@pytest.mark.usefixtures("mongo_test_db")
def test_delete_user(flask_client: Flask, test_user_request: dict[str, str], user_repository: UserRepository) -> None:
    username = test_user_request.get("username")

    user = user_repository.get_user_by_username(username=username)

    id_to_delete = user.get("_id")

    response: Response = flask_client.delete(
        f"{BLUEPRINTS['users']}/delete/{id_to_delete}",
    )

    result = response.json
    status_code = response.status_code

    message = result.get("message")
    data = result.get("data")

    assert status_code == 200
    assert message == f"User with id: {id_to_delete} was deleted."
    assert isinstance(data, dict)

    assert data.get("_id") == str(id_to_delete)
    assert data.get("username") == user.get("username")
    assert data.get("scores") == user.get("scores")
    assert data.get("total_score") == user.get("total_score")

@pytest.mark.usefixtures("mongo_test_db")
def test_delete_user_with_not_found_id(flask_client: Flask) -> None:
    response: Response = flask_client.delete(f"{BLUEPRINTS['users']}/delete/{USER_MOCK['not_found_user_id']}")

    result = response.json
    status_code = response.status_code

    message = result.get("message")
    data = result.get("data")

    assert status_code == 404
    assert message == f"No user found with id: {USER_MOCK['not_found_user_id']}."
    assert not data

@pytest.mark.usefixtures("mongo_test_db")
def test_delete_user_with_wrong_id(flask_client: Flask) -> None:
    response: Response = flask_client.delete(f"{BLUEPRINTS['users']}/delete/{USER_MOCK['wrong_user_id']}")

    result = response.json
    status_code = response.status_code

    message = result.get("message")

    assert status_code == 400
    assert isinstance(message, str)
    assert "Error deleting user:" in message