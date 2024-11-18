from bson import ObjectId

import pytest

from src.data_access.flags_repository import FlagRepository


@pytest.mark.usefixtures("mongo_test_db")
def test_get_all_flags(flag_repository: FlagRepository) -> None:
    flags = flag_repository.get_all_flags()

    assert isinstance(flags, list)

    if flags:
        first_flag = flags[0]
        assert first_flag
        assert first_flag.get("_id")
        assert first_flag.get("name")
        assert first_flag.get("image")

@pytest.mark.usefixtures("mongo_test_db")
def test_insert_and_get_and_delete_flag(flag_repository: FlagRepository, test_flag: dict[str, str]) -> None:
    name = test_flag.get("name")
    image = test_flag.get("image")

    flag_id = flag_repository.insert_flag(flag=test_flag)

    assert flag_id
    assert isinstance(flag_id, str)

    flag_id = ObjectId(flag_id)

    assert isinstance(flag_id, ObjectId)

    flag = flag_repository.get_flag(flag_id=flag_id)

    assert flag
    assert ObjectId(flag.get("_id")) == flag_id
    assert flag.get("name") == name
    assert flag.get("image") == image

    flag_repository.delete_flag_by_id(flag_id=flag_id)

    flag = flag_repository.get_flag(flag_id=flag_id)

    assert not flag

@pytest.mark.usefixtures("mongo_test_db")
def test_get_random_flags_by_quantity(flag_repository: FlagRepository) -> None:
    quantity = 2
    flags = flag_repository.get_random_flags(quantity=quantity)

    assert isinstance(flags, list)

    if flags:
        first_flag = flags[0]
        assert first_flag.get("_id")
        assert first_flag.get("name")
        assert first_flag.get("image")

    assert len(flags) >= 0 and len(flags) <= quantity
    