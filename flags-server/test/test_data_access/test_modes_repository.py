from bson import ObjectId

import pytest

from src.models.Mode import Mode
from src.data_access.modes_repository import ModeRepository

from test.conftest import TEST_MODE_MOCK


@pytest.mark.usefixtures("mongo_test_db", "app_context")
def test_get_all_modes(mode_repository: ModeRepository) -> None:
    modes = mode_repository.get_all_modes()

    assert isinstance(modes, list)

    if modes:
        mode = Mode(**modes[0])

        assert mode.id == modes[0].get("_id")
        assert mode.name == modes[0].get("name")
        assert mode.description == modes[0].get("description")
        assert mode.multiplier == modes[0].get("multiplier")
        assert mode.timeleft == modes[0].get("timeleft")


@pytest.mark.usefixtures("mongo_test_db", "app_context")
def test_insert_get_by_id_delete_mode(mode_repository: ModeRepository, test_mode: dict[str, str]) -> None:
    mode_id = mode_repository.insert_mode(mode=test_mode)

    assert mode_id
    assert isinstance(mode_id, str)

    mode_id = ObjectId(mode_id)

    assert isinstance(mode_id, ObjectId)

    mode = mode_repository.get_mode_by_id(mode_id=mode_id)
    mode = Mode(**mode)

    assert mode

    assert mode.id == mode_id
    assert mode.name == TEST_MODE_MOCK.get("name")
    assert mode.description == TEST_MODE_MOCK.get("description")
    assert mode.multiplier == TEST_MODE_MOCK.get("multiplier")
    assert mode.timeleft == TEST_MODE_MOCK.get("timeleft")

    mode_repository.delete_mode_by_id(mode_id=mode_id)

    mode = mode_repository.get_mode_by_id(mode_id=mode_id)

    assert not mode


@pytest.mark.usefixtures("mongo_test_db", "app_context")
def test_insert_get_by_name_delete_mode(mode_repository: ModeRepository, test_mode: dict[str, str]) -> None:
    mode_id = mode_repository.insert_mode(mode=test_mode)

    assert mode_id
    assert isinstance(mode_id, str)

    mode_id = ObjectId(mode_id)

    assert isinstance(mode_id, ObjectId)

    mode = mode_repository.get_mode_by_name(name=test_mode.get("name"))
    mode = Mode(**mode)

    assert mode

    assert mode.id == mode_id
    assert mode.name == TEST_MODE_MOCK.get("name")
    assert mode.description == TEST_MODE_MOCK.get("description")
    assert mode.multiplier == TEST_MODE_MOCK.get("multiplier")
    assert mode.timeleft == TEST_MODE_MOCK.get("timeleft")

    mode_repository.delete_mode_by_id(mode_id=mode_id)

    mode = mode_repository.get_mode_by_name(name=test_mode.get("name"))

    assert not mode