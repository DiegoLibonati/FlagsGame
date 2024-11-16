from bson import ObjectId

import pytest

from src.models.Flag import Flag
from src.data_access.flags_repository import FlagRepository

from test.conftest import TEST_FLAG_MOCK


@pytest.mark.usefixtures("mongo_test_db", "app_context")
def test_get_all_flags(flag_repository: FlagRepository) -> None:
    flags = flag_repository.get_all_flags()

    assert isinstance(flags, list)

    if flags:
        flag = Flag(**flags[0])

        assert flag.id == flags[0].get("_id")
        assert flag.name == flags[0].get("name")
        assert flag.image == flags[0].get("image")


@pytest.mark.usefixtures("mongo_test_db", "app_context")
def test_insert_get_delete_flag(flag_repository: FlagRepository, test_flag: dict[str, str]) -> None:
    flag_id = flag_repository.insert_flag(flag=test_flag)

    assert flag_id
    assert isinstance(flag_id, str)

    flag_id = ObjectId(flag_id)

    assert isinstance(flag_id, ObjectId)

    flag = flag_repository.get_flag(flag_id=flag_id)
    flag = Flag(**flag)

    assert flag

    assert flag.id == flag_id
    assert flag.name == TEST_FLAG_MOCK.get("name")
    assert flag.image == TEST_FLAG_MOCK.get("image")

    flag_repository.delete_flag_by_id(flag_id=flag_id)

    flag = flag_repository.get_flag(flag_id=flag_id)

    assert not flag


@pytest.mark.usefixtures("mongo_test_db", "app_context")
def test_get_random_flags_by_quantity(flag_repository: FlagRepository) -> None:
    quantity = 2
    flags = flag_repository.get_random_flags(quantity=quantity)

    assert isinstance(flags, list)

    if flags:
        flag = Flag(**flags[0])

        assert flag.id == flags[0].get("_id")
        assert flag.name == flags[0].get("name")
        assert flag.image == flags[0].get("image")

    assert len(flags) >= 0 and len(flags) <= quantity
    