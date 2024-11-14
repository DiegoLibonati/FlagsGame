import pytest

from flask import Flask
from flask import Response

from tests.conftest import prefix_flags_bp
from tests.conftest import test_flag_mock
from tests.conftest import test_mode_name_mock


@pytest.mark.usefixtures("mongo_test_db")
def test_add_flag(flask_client: Flask, test_flag: dict[str, str]) -> None:
    response: Response = flask_client.post(
        f"{prefix_flags_bp}/newflag",
        json=test_flag,
    )
    result = response.json
    status_code = response.status_code

    message = result.get("message")
    flag = result.get("fields")

    inserted_flag_id = flag.get("_id")

    assert status_code == 201
    assert message == "New flag added."
    assert flag == {**test_flag, "_id": inserted_flag_id}

    test_delete_flag(flask_client=flask_client, inserted_flag_id=inserted_flag_id)


@pytest.mark.usefixtures("mongo_test_db")
def test_add_wrong_flag(flask_client: Flask) -> None:
    wrong_flag = {
        "image": "",
        "name": ""
    }

    response: Response = flask_client.post(
        f"{prefix_flags_bp}/newflag",
        json=wrong_flag,
    )
    result = response.json
    status_code = response.status_code

    message = result.get("message")
    flag = result.get("fields")

    assert status_code == 400
    assert message == "The flag could not be added because the fields are not valid."
    assert flag == wrong_flag


@pytest.mark.usefixtures("mongo_test_db")
def test_get_flags(flask_client: Flask, inserted_flag_id: str) -> None:
    response: Response = flask_client.get(
        f"{prefix_flags_bp}/",
    )
    result = response.json
    status_code = response.status_code

    message = result.get("message")
    flags = result.get("data")
    test_flag = {
        **test_flag_mock,
        "_id": inserted_flag_id, 
    }

    assert status_code == 200
    assert message == "The flags were successfully obtained."
    assert type(flags) == list
    assert test_flag in flags

    for flag in flags: 
        assert flag

        if flag.get("_id") == inserted_flag_id:
            assert flag.get("name") == test_flag_mock.get("name")
            assert flag.get("image") == test_flag_mock.get("image")
            continue

        assert flag.get("_id")
        assert flag.get("name")
        assert flag.get("image")

    test_delete_flag(flask_client=flask_client, inserted_flag_id=inserted_flag_id)


@pytest.mark.usefixtures("mongo_test_db")
def test_get_random_flags(flask_client: Flask) -> None:
    response: Response = flask_client.get(
        f"{prefix_flags_bp}/{test_mode_name_mock}",
    )
    result = response.json
    status_code = response.status_code

    message = result.get("message")
    flags = result.get("data")

    assert status_code == 200
    assert message == "The flags were obtained randomly."
    assert type(flags) == list
    assert len(flags) >= 0 and len(flags) <= 5


@pytest.mark.usefixtures("mongo_test_db")
def test_wrong_get_random_flags(flask_client: Flask) -> None:
    wrong_mode_name = "12344321"

    response: Response = flask_client.get(
        f"{prefix_flags_bp}/{wrong_mode_name}",
    )
    result = response.json
    status_code = response.status_code

    message = result.get("message")
    flags = result.get("data")

    assert status_code == 400
    assert message == "The flags could not be obtained randomly."
    assert type(flags) == list
    assert len(flags) == 0


@pytest.mark.usefixtures("mongo_test_db")
def test_delete_flag(flask_client: Flask, inserted_flag_id: str) -> None:
    response: Response = flask_client.delete(f"{prefix_flags_bp}/delete/{inserted_flag_id}")
    result = response.json
    status_code = response.status_code

    message = result.get("message")

    assert status_code == 200
    assert message == f"{inserted_flag_id} was deleted."


@pytest.mark.usefixtures("mongo_test_db")
def test_delete_wrong_flag(flask_client: Flask) -> None:
    response: Response = flask_client.delete(f"{prefix_flags_bp}/delete/asd")
    result = response.json
    status_code = response.status_code

    message = result.get("message")

    assert status_code == 400
    assert type(message) == str