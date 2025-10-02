from unittest.mock import patch

from src.constants.defaults import DEFAULT_MODES
from src.models.mode_model import ModeModel
from src.services.mode_service import ModeService
from src.startup.init_modes import add_default_modes


def test_add_default_modes_when_modes_exist() -> None:
    with patch.object(
        ModeService, "get_all_modes", return_value=[{"name": "Arcade"}]
    ) as mock_get, patch.object(ModeService, "add_mode") as mock_add:
        add_default_modes()

        mock_get.assert_called_once()
        mock_add.assert_not_called()


def test_add_default_modes_when_no_modes() -> None:
    with patch.object(
        ModeService, "get_all_modes", return_value=[]
    ) as mock_get, patch.object(ModeService, "add_mode") as mock_add:
        add_default_modes()

        mock_get.assert_called_once()
        assert mock_add.call_count == len(DEFAULT_MODES)

        for call in mock_add.call_args_list:
            args, _ = call
            assert isinstance(args[0], ModeModel)


def test_add_default_modes_idempotent() -> None:
    with patch.object(
        ModeService, "get_all_modes", side_effect=[[], [{}]]
    ) as mock_get, patch.object(ModeService, "add_mode") as mock_add:
        add_default_modes()
        add_default_modes()

        assert mock_add.call_count == len(DEFAULT_MODES)
        assert mock_get.call_count == 2
