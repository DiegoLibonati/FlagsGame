import pytest

from flask import Flask
from flask import Response

from test.constants import BLUEPRINTS
from test.constants import MODE_MOCK


@pytest.mark.usefixtures("mongo_test_db")
def test_add_mode(flask_client: Flask, test_mode: dict[str, str]) -> None:
    name = test_mode.get("name")
    description = test_mode.get("description")
    multiplier = test_mode.get("multiplier")
    timeleft = test_mode.get("timeleft")

    response: Response = flask_client.post(
        f"{BLUEPRINTS['modes']}/newmode",
        json=test_mode
    )

    result = response.json
    status_code = response.status_code

    message = result.get("message")
    data = result.get("data")

    assert status_code == 201
    assert message == "Successfully created new mode."
    assert isinstance(data, dict)
    assert data.get("name") == name
    assert data.get("description") == description
    assert data.get("multiplier") == multiplier
    assert data.get("timeleft") == timeleft

@pytest.mark.usefixtures("mongo_test_db")
def test_add_mode_with_wrong_mode(flask_client: Flask, test_mode: dict[str, str]) -> None:
    name = test_mode.get("name")
    description = test_mode.get("description")
    timeleft = test_mode.get("timeleft")

    response: Response = flask_client.post(
        f"{BLUEPRINTS['modes']}/newmode",
        json={
            "name": name,
            "description": description,
            "multiplier": "",
            "timeleft": timeleft
        }
    )

    result = response.json
    status_code = response.status_code

    message = result.get("message")
    data = result.get("data")

    assert status_code == 400
    assert message == "The mode could not be added because the fields entered are not valid."
    assert not data

@pytest.mark.usefixtures("mongo_test_db")
def test_get_modes(flask_client: Flask, test_mode: dict[str, str]) -> None:
    name = test_mode.get("name")
    description = test_mode.get("description")
    multiplier = test_mode.get("multiplier")
    timeleft = test_mode.get("timeleft")

    response: Response = flask_client.get(
        f"{BLUEPRINTS['modes']}/",
    )

    result = response.json
    status_code = response.status_code

    message = result.get("message")
    data = result.get("data")

    assert message == "Successfully obtained modes."
    assert status_code == 200
    assert isinstance(data, list)
    assert len(data) >= 1

    for mode in data:
        if mode.get("name") == name:
            assert mode
            assert mode.get("_id")
            assert mode.get("name") == name
            assert mode.get("description") == description
            assert mode.get("multiplier") == multiplier
            assert mode.get("timeleft") == timeleft

@pytest.mark.usefixtures("mongo_test_db")
def test_find_mode(flask_client: Flask, test_mode: dict[str, str]) -> None:
    name = test_mode.get("name")
    description = test_mode.get("description")
    multiplier = test_mode.get("multiplier")
    timeleft = test_mode.get("timeleft")

    response: Response = flask_client.get(
        f"{BLUEPRINTS['modes']}/findmode/{name}",
    )

    result = response.json
    status_code = response.status_code

    message = result.get("message")
    data = result.get("data")

    assert status_code == 200
    assert message == "Successfully obtained the requested mode."
    assert isinstance(data, dict)
    assert data.get("_id")
    assert data.get("name") == name
    assert data.get("description") == description
    assert data.get("multiplier") == multiplier
    assert data.get("timeleft") == timeleft

@pytest.mark.usefixtures("mongo_test_db")
def test_find_mode_not_name(flask_client: Flask) -> None:
    response: Response = flask_client.get(
        f"{BLUEPRINTS['modes']}/findmode/",
    )

    status_code = response.status_code

    assert status_code == 404

@pytest.mark.usefixtures("mongo_test_db")
def test_find_mode_not_found_mode(flask_client: Flask) -> None:
    response: Response = flask_client.get(
        f"{BLUEPRINTS['modes']}/findmode/{MODE_MOCK['not_found_mode_name']}",
    )

    result = response.json
    status_code = response.status_code

    message = result.get("message")
    data = result.get("data")

    assert status_code == 404
    assert message == f"A game mode with name {MODE_MOCK['not_found_mode_name']} was not found, please enter valid fields."
    assert not data

@pytest.mark.usefixtures("mongo_test_db")
def test_get_mode_top(flask_client: Flask, test_mode: dict[str, str]) -> None:
    name = test_mode.get("name")

    response: Response = flask_client.get(
        f"{BLUEPRINTS['modes']}/mode/top/{name}",
    )

    result = response.json
    status_code = response.status_code

    message = result.get("message")
    data = result.get("data")

    assert status_code == 200
    assert message == "The top ten of the requested mode was obtained."
    assert isinstance(data, list)
    assert len(data) >= 0 and len(data) <= 10

    for user in data:
        assert user
        assert user.get("_id")
        assert user.get("username")
        assert not user.get("score") if not user.get("score") else user.get("score")

    if len(data) >= 2:
        first_user = data[0]
        second_user = data[1]

        assert first_user.get("score") >= second_user.get("score")

@pytest.mark.usefixtures("mongo_test_db")
def test_get_mode_not_found_mode_name(flask_client: Flask) -> None:
    response: Response = flask_client.get(
        f"{BLUEPRINTS['modes']}/mode/top/{MODE_MOCK['not_found_mode_name']}",
    )

    result = response.json
    status_code = response.status_code

    message = result.get("message")
    data = result.get("data")

    assert status_code == 404
    assert message == "The top could not be obtained as requested."
    assert not data

@pytest.mark.usefixtures("mongo_test_db")
def test_delete_mode(flask_client: Flask, test_mode: dict[str, str]) -> None:
    name = test_mode.get("name")
    description = test_mode.get("description")
    multiplier = test_mode.get("multiplier")
    timeleft = test_mode.get("timeleft")

    response: Response = flask_client.get(
        f"{BLUEPRINTS['modes']}/findmode/{name}",
    )

    result = response.json
    id_to_delete = result["data"].get("_id")

    response: Response = flask_client.delete(
        f"{BLUEPRINTS['modes']}/delete/{id_to_delete}",
    )

    result = response.json
    status_code = response.status_code

    message = result.get("message")
    data = result.get("data")

    assert status_code == 200
    assert message == f"Mode with id: {id_to_delete} was deleted."
    assert isinstance(data, dict)

    assert data.get("_id") == id_to_delete
    assert data.get("name") == name
    assert data.get("description") == description
    assert data.get("multiplier") == multiplier
    assert data.get("timeleft") == timeleft

@pytest.mark.usefixtures("mongo_test_db")
def test_delete_mode_with_not_found_id(flask_client: Flask) -> None:
    response: Response = flask_client.delete(f"{BLUEPRINTS['modes']}/delete/{MODE_MOCK['not_found_mode_id']}")

    result = response.json
    status_code = response.status_code

    message = result.get("message")
    data = result.get("data")

    assert status_code == 404
    assert message == f"No mode found with id: {MODE_MOCK['not_found_mode_id']}."
    assert not data

@pytest.mark.usefixtures("mongo_test_db")
def test_delete_mode_with_wrong_id(flask_client: Flask) -> None:
    response: Response = flask_client.delete(f"{BLUEPRINTS['modes']}/delete/{MODE_MOCK['wrong_mode_id']}")

    result = response.json
    status_code = response.status_code

    message = result.get("message")

    assert status_code == 400
    assert isinstance(message, str)
    assert "Error deleting mode:" in message