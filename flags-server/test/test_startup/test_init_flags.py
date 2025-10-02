from unittest.mock import patch

from src.constants.defaults import DEFAULT_FLAGS
from src.models.flag_model import FlagModel
from src.services.flag_service import FlagService
from src.startup.init_flags import add_default_flags


def test_add_default_flags_when_flags_exist() -> None:
    with patch.object(
        FlagService, "get_all_flags", return_value=[{"name": "Argentina"}]
    ) as mock_get, patch.object(FlagService, "add_flag") as mock_add:
        add_default_flags()

        mock_get.assert_called_once()
        mock_add.assert_not_called()


def test_add_default_flags_when_no_flags() -> None:
    with patch.object(
        FlagService, "get_all_flags", return_value=[]
    ) as mock_get, patch.object(FlagService, "add_flag") as mock_add:
        add_default_flags()

        mock_get.assert_called_once()
        assert mock_add.call_count == len(DEFAULT_FLAGS)

        for call in mock_add.call_args_list:
            args, _ = call
            assert isinstance(args[0], FlagModel)


def test_add_default_flags_idempotent() -> None:
    with patch.object(
        FlagService, "get_all_flags", side_effect=[[], [{}]]
    ) as mock_get, patch.object(FlagService, "add_flag") as mock_add:
        add_default_flags()
        add_default_flags()

        assert mock_add.call_count == len(DEFAULT_FLAGS)
        assert mock_get.call_count == 2
