from bson import ObjectId

from src.models.Flag import Flag

from test.constants import FLAG_MOCK


def test_flag_model(flag_model: Flag) -> None:
    _id = FLAG_MOCK['flag'].get("_id")
    name = FLAG_MOCK['flag'].get("name")
    image = FLAG_MOCK['flag'].get("image")

    assert flag_model.id == ObjectId(_id)
    assert flag_model.name == name
    assert flag_model.image == image

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
