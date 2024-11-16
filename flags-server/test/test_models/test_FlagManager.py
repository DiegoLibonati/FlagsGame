from src.models.Flag import Flag
from src.models.FlagManager import FlagManager

from test.conftest import TEST_FLAG_MOCK

def test_flag_manager_add_flag(flag_manager_model: FlagManager, flag_model: Flag) -> None:
    assert not flag_manager_model.flags

    flag_manager_model.add_flag(flag=flag_model)

    assert flag_manager_model.flags
    assert flag_model in flag_manager_model.flags

def test_flag_manager_parse_flags(flag_manager_model: FlagManager, flag_model: Flag) -> None:
    assert flag_manager_model.flags
    assert flag_model in flag_manager_model.flags

    parsed_flags = flag_manager_model.parse_flags()

    assert isinstance(parsed_flags, list)

    for flag in parsed_flags:
        assert isinstance(flag, dict)
        assert flag.get("name") == TEST_FLAG_MOCK.get("name")
        assert flag.get("image") == TEST_FLAG_MOCK.get("image")