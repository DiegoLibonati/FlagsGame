import logging

import pytest

from flask import Flask
from flask import Response

from test.constants import PREFIX_FLAGS_BP
from test.constants import NOT_FOUND_ID_FLAG
from test.constants import WRONG_ID_FLAG


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@pytest.mark.usefixtures("mongo_test_db")
def test_add_flag(flask_client: Flask, test_flag: dict[str, str]) -> None:
    name = test_flag.get("name")
    image = test_flag.get("image")

    response: Response = flask_client.post(
        f"{PREFIX_FLAGS_BP}/newflag",
        json=test_flag,
    )

    result = response.json
    status_code = response.status_code

    message = result.get("message")
    data = result.get("data")

    assert status_code == 201
    assert message == "New flag added."
    assert isinstance(data, dict)
    assert data
    assert data.get("name") == name
    assert data.get("image") == image

@pytest.mark.usefixtures("mongo_test_db")
def test_add_flag_with_wrong_flag(flask_client: Flask) -> None:
    wrong_flag = {
        "image": "12.png",
        "name": ""
    }

    response: Response = flask_client.post(
        f"{PREFIX_FLAGS_BP}/newflag",
        json=wrong_flag,
    )

    result = response.json
    status_code = response.status_code

    message = result.get("message")
    data = result.get("data")

    assert status_code == 400
    assert message == "The flag could not be added because the fields are not valid."
    assert not data

@pytest.mark.usefixtures("mongo_test_db")
def test_get_flags(flask_client: Flask, test_flag: dict[str, str]) -> None:
    name = test_flag.get("name")
    image = test_flag.get("image")

    response: Response = flask_client.get(
        f"{PREFIX_FLAGS_BP}/",
    )

    result = response.json
    status_code = response.status_code

    message = result.get("message")
    data = result.get("data")

    assert status_code == 200
    assert message == "The flags were successfully obtained."
    assert isinstance(data, list)

    for flag in data: 
        assert flag
        assert flag.get("_id")
        
        if flag.get("name") == name:
            assert flag.get("name") == name
            assert flag.get("image") == image

@pytest.mark.usefixtures("mongo_test_db")
def test_get_random_flags(flask_client: Flask) -> None:
    quantity = 5

    response: Response = flask_client.get(
        f"{PREFIX_FLAGS_BP}/random/{quantity}",
    )

    result = response.json
    status_code = response.status_code

    message = result.get("message")
    data = result.get("data")

    assert status_code == 200
    assert message == "The flags were obtained randomly."
    assert isinstance(data, list)
    assert len(data) >= 0 and len(data) <= quantity

    for flag in data:
        assert flag
        assert flag.get("_id")
        assert flag.get("name")
        assert flag.get("image")

@pytest.mark.usefixtures("mongo_test_db")
def test_get_random_flags_with_invalid_int_passing_str(flask_client: Flask) -> None:
    quantity = "asd"

    response: Response = flask_client.get(
        f"{PREFIX_FLAGS_BP}/random/{quantity}",
    )

    result = response.json
    status_code = response.status_code

    message = result.get("message")
    data = result.get("data")

    assert status_code == 400
    assert message == "Invalid quantity. It must be a positive integer."
    assert isinstance(data, list)
    assert not data

@pytest.mark.usefixtures("mongo_test_db")
def test_get_random_flags_with_invalid_int_passing_negative(flask_client: Flask) -> None:
    quantity = -1

    response: Response = flask_client.get(
        f"{PREFIX_FLAGS_BP}/random/{quantity}",
    )

    result = response.json
    status_code = response.status_code

    message = result.get("message")
    data = result.get("data")

    assert status_code == 400
    assert message == "Invalid quantity. It must be a positive integer."
    assert isinstance(data, list)
    assert not data

@pytest.mark.usefixtures("mongo_test_db")
def test_delete_flag(flask_client: Flask, test_flag: dict[str, str]) -> None:
    name = test_flag.get("name")
    image = test_flag.get("image")

    response: Response = flask_client.get(
        f"{PREFIX_FLAGS_BP}/",
    )

    result = response.json
    flag_to_delete = [flag for flag in result.get("data") if flag.get("name") == name and flag.get("image") == image][0]

    assert flag_to_delete

    id_to_delete = flag_to_delete.get("_id")

    response: Response = flask_client.delete(f"{PREFIX_FLAGS_BP}/delete/{id_to_delete}")

    result = response.json
    status_code = response.status_code

    message = result.get("message")
    data = result.get("data")

    assert status_code == 200
    assert message == f"Flag with id: {id_to_delete} was deleted."
    assert isinstance(data, dict)

    assert data.get("_id") == id_to_delete
    assert data.get("name") == name
    assert data.get("image") == image

@pytest.mark.usefixtures("mongo_test_db")
def test_delete_flag_with_not_found_id(flask_client: Flask) -> None:
    response: Response = flask_client.delete(f"{PREFIX_FLAGS_BP}/delete/{NOT_FOUND_ID_FLAG}")

    result = response.json
    status_code = response.status_code

    message = result.get("message")
    data = result.get("data")

    assert status_code == 404
    assert message == f"No flag found with id: {NOT_FOUND_ID_FLAG}."
    assert isinstance(message, str)
    assert not data

@pytest.mark.usefixtures("mongo_test_db")
def test_delete_flag_with_wrong_id(flask_client: Flask) -> None:
    response: Response = flask_client.delete(f"{PREFIX_FLAGS_BP}/delete/{WRONG_ID_FLAG}")

    result = response.json
    status_code = response.status_code

    message = result.get("message")

    assert status_code == 400
    assert isinstance(message, str)
    assert "Error deleting flag:" in message