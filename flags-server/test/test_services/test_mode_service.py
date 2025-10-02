from unittest.mock import patch

import pytest
from bson import ObjectId

from src.models.mode_model import ModeModel
from src.services.mode_service import ModeService
from src.utils.exceptions import ConflictAPIError, NotFoundAPIError


class DummyInsertOneResult:
    def __init__(self, inserted_id: ObjectId) -> None:
        self.inserted_id: ObjectId = inserted_id


class DummyDeleteResult:
    def __init__(self, deleted_count: int) -> None:
        self.deleted_count: int = deleted_count


def test_add_mode_success() -> None:
    mode = ModeModel(name="Arcade", description="Fast mode", multiplier=2, timeleft=90)

    with patch(
        "src.services.mode_service.ModeDAO.find_one_by_name", return_value=None
    ), patch(
        "src.services.mode_service.ModeDAO.insert_one",
        return_value=DummyInsertOneResult(ObjectId()),
    ):
        res = ModeService.add_mode(mode)

    assert isinstance(res, DummyInsertOneResult)
    assert res.inserted_id is not None


def test_add_mode_conflict() -> None:
    mode = ModeModel(name="Arcade", description="Fast mode", multiplier=2, timeleft=90)

    with patch(
        "src.services.mode_service.ModeDAO.find_one_by_name",
        return_value={"name": "Arcade"},
    ):
        with pytest.raises(ConflictAPIError):
            ModeService.add_mode(mode)


def test_get_all_modes() -> None:
    mock_modes: list[dict[str, str | int]] = [
        {
            "_id": "1",
            "name": "Arcade",
            "description": "Fast",
            "multiplier": 2,
            "timeleft": 90,
        }
    ]

    with patch("src.services.mode_service.ModeDAO.find", return_value=mock_modes):
        res = ModeService.get_all_modes()

    assert res == mock_modes
    assert res[0]["name"] == "Arcade"


def test_get_mode_by_id() -> None:
    _id: ObjectId = ObjectId()
    mock_mode: dict[str, str | int] = {
        "_id": str(_id),
        "name": "Classic",
        "description": "Normal",
        "multiplier": 1,
        "timeleft": 60,
    }

    with patch(
        "src.services.mode_service.ModeDAO.find_one_by_id", return_value=mock_mode
    ):
        res = ModeService.get_mode_by_id(_id)

    assert res == mock_mode
    assert res["name"] == "Classic"


def test_get_mode_by_name() -> None:
    mock_mode: dict[str, str | int] = {
        "_id": "1",
        "name": "Survival",
        "description": "Hardcore",
        "multiplier": 3,
        "timeleft": 120,
    }

    with patch(
        "src.services.mode_service.ModeDAO.find_one_by_name", return_value=mock_mode
    ):
        res = ModeService.get_mode_by_name("Survival")

    assert res == mock_mode
    assert res["name"] == "Survival"


def test_delete_mode_success() -> None:
    _id: ObjectId = ObjectId()

    with patch(
        "src.services.mode_service.ModeDAO.find_one_by_id",
        return_value={"_id": str(_id), "name": "Arcade"},
    ), patch(
        "src.services.mode_service.ModeDAO.delete_one_by_id",
        return_value=DummyDeleteResult(1),
    ):
        res = ModeService.delete_mode_by_id(_id)

    assert isinstance(res, DummyDeleteResult)
    assert res.deleted_count == 1


def test_delete_mode_not_found() -> None:
    _id: ObjectId = ObjectId()

    with patch("src.services.mode_service.ModeDAO.find_one_by_id", return_value=None):
        with pytest.raises(NotFoundAPIError):
            ModeService.delete_mode_by_id(_id)
