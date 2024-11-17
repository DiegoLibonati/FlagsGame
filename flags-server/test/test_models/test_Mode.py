from bson import ObjectId

from src.models.Mode import Mode

from test.constants import TEST_MODE_MOCK


def test_mode_model(mode_model: Mode) -> None:
    _id = TEST_MODE_MOCK.get("_id")
    name = TEST_MODE_MOCK.get("name")
    description = TEST_MODE_MOCK.get("description")
    multiplier = TEST_MODE_MOCK.get("multiplier")
    timeleft = TEST_MODE_MOCK.get("timeleft")


    assert mode_model.id == ObjectId(_id)
    assert mode_model.name == name
    assert mode_model.description == description
    assert mode_model.multiplier == multiplier
    assert mode_model.timeleft == timeleft

def test_mode_to_dict(mode_model: Mode) -> None:
    mode_dict = mode_model.to_dict()

    assert isinstance(mode_dict, dict)
    assert mode_dict.get("_id") == str(mode_model.id)
    assert mode_dict.get("name") == mode_model.name
    assert mode_dict.get("description") == mode_model.description
    assert mode_dict.get("multiplier") == mode_model.multiplier
    assert mode_dict.get("timeleft") == mode_model.timeleft
