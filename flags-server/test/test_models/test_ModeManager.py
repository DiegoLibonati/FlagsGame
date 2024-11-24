from typing import Any

import pytest

from src.models.Mode import Mode
from src.models.ModeManager import ModeManager

from test.constants import MODE_MOCK


def test_init_mode_manager(mode_manager_model: ModeManager, test_modes: dict[str, Any]) -> None:
    assert mode_manager_model
    assert not mode_manager_model.modes
    assert mode_manager_model.initializer(**test_modes[0])

def test_add_mode(mode_manager_model: ModeManager, mode_model: Mode) -> None:
    mode_manager_model.add_mode(mode=mode_model)

    assert mode_manager_model.modes
    assert mode_model in mode_manager_model.modes

def test_add_mode_with_wrong_mode(mode_manager_model: ModeManager) -> None:
    with pytest.raises(TypeError) as exc_info:
        mode_manager_model.add_mode(mode={"pepe": "123"})

    assert str(exc_info.value) == "You must enter a valid mode in order to add it."

def test_add_modes(mode_manager_model: ModeManager, test_modes: dict[str, Any]) -> None:
    mode_manager_model.add_modes(modes=test_modes)

    assert mode_manager_model.modes
    
    for mode in mode_manager_model.modes:
        if str(mode.id) == MODE_MOCK['not_found_mode_id']: continue
        assert mode.to_dict() in test_modes

def test_add_modes_with_wrong_modes(mode_manager_model: ModeManager) -> None:
    with pytest.raises(TypeError) as exc_info:
        mode_manager_model.add_modes(modes={})

    assert str(exc_info.value) == "You must enter a valid modes to add its."

def test_get_modes_name(mode_manager_model: ModeManager, mode_model: Mode) -> None:
    mode_names = mode_manager_model.get_modes_names()

    assert mode_names
    assert isinstance(mode_names, list)
    assert mode_model.name.lower() in mode_names

def test_parse_modes(mode_manager_model: ModeManager) -> None:
    parsed_modes = mode_manager_model.parse_items()

    assert isinstance(parsed_modes, list)

    for mode in parsed_modes:
        assert isinstance(mode, dict)
        assert mode.get("_id")
        assert mode.get("name")
        assert mode.get("description")
        assert mode.get("multiplier")
        assert mode.get("timeleft")