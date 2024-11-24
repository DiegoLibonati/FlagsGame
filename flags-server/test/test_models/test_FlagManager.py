import logging

from typing import Any

import pytest

from src.models.Flag import Flag
from src.models.FlagManager import FlagManager

from test.constants import FLAG_MOCK


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def test_init_mode_manager(flag_manager_model: FlagManager, test_flags: dict[str, Any]) -> None:
    assert flag_manager_model
    assert not flag_manager_model.flags
    assert flag_manager_model.initializer(**test_flags[0])

def test_add_flag(flag_manager_model: FlagManager, flag_model: Flag) -> None:
    flag_manager_model.add_flag(flag=flag_model)

    assert flag_manager_model.flags
    assert flag_model in flag_manager_model.flags

def test_add_flag_with_wrong_flag(flag_manager_model: FlagManager) -> None:
    with pytest.raises(TypeError) as exc_info:
        flag_manager_model.add_flag(flag={"pepe": "123"})

    assert str(exc_info.value) == "You must enter a valid flag in order to add it."

def test_add_flags(flag_manager_model: FlagManager, test_flags: dict[str, str]) -> None:
    flag_manager_model.add_flags(flags=test_flags)

    assert flag_manager_model.flags
    
    for flag in flag_manager_model.flags:
        if str(flag.id) == FLAG_MOCK['not_found_flag_id']: continue
        assert flag.to_dict() in test_flags

def test_add_flags_with_wrong_flags(flag_manager_model: FlagManager) -> None:
    with pytest.raises(TypeError) as exc_info:
        flag_manager_model.add_flags(flags={})

    assert str(exc_info.value) == "You must enter a valid flags to add its."

def test_parse_flags(flag_manager_model: FlagManager) -> None:
    parsed_flags = flag_manager_model.parse_items()

    assert isinstance(parsed_flags, list)

    for flag in parsed_flags:
        assert isinstance(flag, dict)
        assert flag.get("_id")
        assert flag.get("name")
        assert flag.get("image")