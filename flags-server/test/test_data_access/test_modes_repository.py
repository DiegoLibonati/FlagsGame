from bson import ObjectId

import pytest

from src.models.Mode import Mode
from src.data_access.modes_repository import ModeRepository


@pytest.mark.usefixtures("mongo_test_db", "app_context")
def test_get_all_modes(mode_repository: ModeRepository) -> None:
    modes = mode_repository.get_all_modes()

    assert isinstance(modes, list)

    if modes:
        first_mode = modes[0]

        _id = first_mode.get("_id")
        name = first_mode.get("name")
        description = first_mode.get("description")
        multiplier = first_mode.get("multiplier")
        timeleft = first_mode.get("timeleft")

        mode = Mode(**first_mode)

        assert mode.id == _id
        assert mode.name == name
        assert mode.description == description
        assert mode.multiplier == multiplier
        assert mode.timeleft == timeleft


@pytest.mark.usefixtures("mongo_test_db", "app_context")
def test_insert_and_get_and_delete_mode_by_id(mode_repository: ModeRepository, test_mode: dict[str, str]) -> None:
    name = test_mode.get("name")
    description = test_mode.get("description")
    multiplier = test_mode.get("multiplier")
    timeleft = test_mode.get("timeleft")

    mode_id = mode_repository.insert_mode(mode=test_mode)

    assert mode_id
    assert isinstance(mode_id, str)

    mode_id = ObjectId(mode_id)

    assert isinstance(mode_id, ObjectId)

    mode = mode_repository.get_mode_by_id(mode_id=mode_id)
    mode = Mode(**mode)

    assert mode
    assert mode.id == mode_id
    assert mode.name == name
    assert mode.description == description
    assert mode.multiplier == multiplier
    assert mode.timeleft == timeleft

    mode_repository.delete_mode_by_id(mode_id=mode_id)

    mode = mode_repository.get_mode_by_id(mode_id=mode_id)

    assert not mode


@pytest.mark.usefixtures("mongo_test_db", "app_context")
def test_insert_and_get_and_delete_mode_by_name(mode_repository: ModeRepository, test_mode: dict[str, str]) -> None:
    name = test_mode.get("name")
    description = test_mode.get("description")
    multiplier = test_mode.get("multiplier")
    timeleft = test_mode.get("timeleft")

    mode_id = mode_repository.insert_mode(mode=test_mode)

    assert mode_id
    assert isinstance(mode_id, str)

    mode_id = ObjectId(mode_id)

    assert isinstance(mode_id, ObjectId)

    mode = mode_repository.get_mode_by_name(name=name)
    mode = Mode(**mode)

    assert mode

    assert mode.id == mode_id
    assert mode.name == name
    assert mode.description == description
    assert mode.multiplier == multiplier
    assert mode.timeleft == timeleft

    mode_repository.delete_mode_by_id(mode_id=mode_id)

    mode = mode_repository.get_mode_by_name(name=name)

    assert not mode