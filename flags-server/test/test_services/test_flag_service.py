from unittest.mock import patch

import pytest
from bson import ObjectId

from src.models.flag_model import FlagModel
from src.services.flag_service import FlagService
from src.utils.exceptions import ConflictAPIError, NotFoundAPIError


class DummyInsertOneResult:
    def __init__(self, inserted_id: ObjectId) -> None:
        self.inserted_id: ObjectId = inserted_id


class DummyDeleteResult:
    def __init__(self, deleted_count: int) -> None:
        self.deleted_count: int = deleted_count


def test_add_flag_success() -> None:
    flag = FlagModel(name="Argentina", image="arg.png")

    with patch(
        "src.services.flag_service.FlagDAO.find_one_by_name", return_value=None
    ), patch(
        "src.services.flag_service.FlagDAO.insert_one",
        return_value=DummyInsertOneResult(ObjectId()),
    ):
        res = FlagService.add_flag(flag)

    assert isinstance(res, DummyInsertOneResult)
    assert res.inserted_id is not None


def test_add_flag_conflict() -> None:
    flag = FlagModel(name="Argentina", image="arg.png")

    with patch(
        "src.services.flag_service.FlagDAO.find_one_by_name",
        return_value={"name": "Argentina"},
    ):
        with pytest.raises(ConflictAPIError):
            FlagService.add_flag(flag)


def test_get_all_flags() -> None:
    mock_flags: list[dict[str, str]] = [
        {"_id": "1", "name": "Argentina", "image": "arg.png"}
    ]

    with patch("src.services.flag_service.FlagDAO.find", return_value=mock_flags):
        res = FlagService.get_all_flags()

    assert res == mock_flags
    assert res[0]["name"] == "Argentina"


def test_get_random_flags() -> None:
    mock_flags: list[dict[str, str]] = [
        {"_id": "1", "name": "Brazil", "image": "bra.png"}
    ]

    with patch(
        "src.services.flag_service.FlagDAO.find_random", return_value=mock_flags
    ):
        res = FlagService.get_random_flags(1)

    assert len(res) == 1
    assert res[0]["name"] == "Brazil"


def test_delete_flag_success() -> None:
    _id: ObjectId = ObjectId()

    with patch(
        "src.services.flag_service.FlagDAO.find_one_by_id",
        return_value={"_id": str(_id), "name": "Chile"},
    ), patch(
        "src.services.flag_service.FlagDAO.delete_one_by_id",
        return_value=DummyDeleteResult(1),
    ):
        res = FlagService.delete_flag_by_id(_id)

    assert isinstance(res, DummyDeleteResult)
    assert res.deleted_count == 1


def test_delete_flag_not_found() -> None:
    _id: ObjectId = ObjectId()

    with patch("src.services.flag_service.FlagDAO.find_one_by_id", return_value=None):
        with pytest.raises(NotFoundAPIError):
            FlagService.delete_flag_by_id(_id)
