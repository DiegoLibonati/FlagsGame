import logging

from src.models.Flag import Flag
from src.models.FlagManager import FlagManager

from test.constants import NOT_FOUND_ID_FLAG


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def test_flag_manager_add_flag(flag_manager_model: FlagManager, flag_model: Flag) -> None:
    assert not flag_manager_model.flags

    flag_manager_model.add_flag(flag=flag_model)

    assert flag_manager_model.flags
    assert flag_model in flag_manager_model.flags

def test_flag_manager_add_flags(flag_manager_model: FlagManager, test_flags: dict[str, str]) -> None:
    flag_manager_model.add_flags(flags=test_flags)

    assert flag_manager_model.flags
    
    for flag in flag_manager_model.flags:
        if str(flag.id) == NOT_FOUND_ID_FLAG: continue
        assert flag.to_dict() in test_flags

def test_flag_manager_parse_flags(flag_manager_model: FlagManager, flag_model: Flag) -> None:
    assert flag_manager_model.flags
    assert flag_model in flag_manager_model.flags

    parsed_flags = flag_manager_model.parse_items()

    assert isinstance(parsed_flags, list)

    for flag in parsed_flags:
        assert isinstance(flag, dict)
        assert flag.get("_id")
        assert flag.get("name")
        assert flag.get("image")