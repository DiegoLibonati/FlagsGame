from bson import ObjectId

import pytest

from src.data_access.modes_repository import ModeRepository


@pytest.mark.usefixtures("mongo_test_db", "app_context")
def test_get_all_modes(mode_repository: ModeRepository) -> None:
    modes = mode_repository.get_all_modes()

    assert isinstance(modes, list)

    if modes:
        first_mode = modes[0]

        assert first_mode
        assert first_mode.get("_id")
        assert first_mode.get("name")
        assert first_mode.get("description")
        assert first_mode.get("multiplier")
        assert first_mode.get("timeleft")

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

    assert mode
    assert ObjectId(mode.get("_id")) == mode_id
    assert mode.get("name") == name
    assert mode.get("description") == description
    assert mode.get("multiplier") == multiplier
    assert mode.get("timeleft") == timeleft

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

    assert mode
    assert ObjectId(mode.get("_id")) == mode_id
    assert mode.get("name") == name
    assert mode.get("description") == description
    assert mode.get("multiplier") == multiplier
    assert mode.get("timeleft") == timeleft

    mode_repository.delete_mode_by_id(mode_id=mode_id)

    mode = mode_repository.get_mode_by_name(name=name)

    assert not mode