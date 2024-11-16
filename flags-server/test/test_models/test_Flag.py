from bson import ObjectId

from src.models.Flag import Flag

from test.conftest import TEST_FLAG_MOCK


def test_flag_model(flag_model: Flag) -> None:
    assert flag_model.id == ObjectId(TEST_FLAG_MOCK.get("_id"))
    assert flag_model.name == TEST_FLAG_MOCK.get("name")
    assert flag_model.image == TEST_FLAG_MOCK.get("image")

def test_flag_is_valid(flag_model: Flag) -> None:
    assert flag_model.is_valid

def test_flag_is_not_valid(not_valid_flag_model: Flag) -> None:
    assert not not_valid_flag_model.is_valid

def test_flag_to_dict(flag_model: Flag) -> None:
    flag_dict = flag_model.to_dict()

    assert isinstance(flag_dict, dict)
    assert flag_dict.get("_id") == str(flag_model.id)
    assert flag_dict.get("name") == flag_model.name
    assert flag_dict.get("image") == flag_model.image
