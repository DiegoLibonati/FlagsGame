from unittest.mock import patch

import pytest
from bson import ObjectId

from src.models.user_model import UserModel
from src.services.user_service import UserService
from src.utils.exceptions import ConflictAPIError, NotFoundAPIError


class DummyInsertOneResult:
    def __init__(self, inserted_id: ObjectId) -> None:
        self.inserted_id: ObjectId = inserted_id


class DummyDeleteResult:
    def __init__(self, deleted_count: int) -> None:
        self.deleted_count: int = deleted_count


class DummyUpdateResult:
    def __init__(self, modified_count: int) -> None:
        self.modified_count: int = modified_count


def test_add_user_success() -> None:
    user = UserModel(
        username="alice", password="pwd123", scores={"General": 10}, total_score=10
    )

    with patch(
        "src.services.user_service.UserDAO.find_one_by_username", return_value=None
    ), patch(
        "src.services.user_service.UserDAO.insert_one",
        return_value=DummyInsertOneResult(ObjectId()),
    ):
        res = UserService.add_user(user)

    assert isinstance(res, DummyInsertOneResult)
    assert res.inserted_id is not None


def test_add_user_conflict() -> None:
    user = UserModel(
        username="bob", password="pwd123", scores={"General": 20}, total_score=20
    )

    with patch(
        "src.services.user_service.UserDAO.find_one_by_username",
        return_value={"username": "bob"},
    ):
        with pytest.raises(ConflictAPIError):
            UserService.add_user(user)


def test_get_all_users() -> None:
    mock_users = [
        {"_id": "1", "username": "alice", "total_score": 50, "scores": {"General": 50}}
    ]

    with patch("src.services.user_service.UserDAO.find", return_value=mock_users):
        res = UserService.get_all_users()

    assert res == mock_users
    assert res[0]["username"] == "alice"


def test_get_user_by_username() -> None:
    mock_user = {
        "_id": "1",
        "username": "bob",
        "total_score": 30,
        "scores": {"General": 30},
    }

    with patch(
        "src.services.user_service.UserDAO.find_one_by_username", return_value=mock_user
    ):
        res = UserService.get_user_by_username("bob")

    assert res == mock_user
    assert res["username"] == "bob"


def test_get_top_users_general() -> None:
    mock_users = [
        {
            "_id": "1",
            "username": "alice",
            "total_score": 100,
            "scores": {"General": 100},
        },
        {"_id": "2", "username": "bob", "total_score": 50, "scores": {"General": 50}},
    ]

    with patch(
        "src.services.user_service.UserService.get_all_users", return_value=mock_users
    ):
        res = UserService.get_top_users("General")

    assert len(res) == 2
    assert res[0]["username"] == "alice"
    assert res[0]["score"] == 100


def test_get_top_users_mode_name() -> None:
    mock_users = [
        {
            "_id": "1",
            "username": "charlie",
            "total_score": 200,
            "scores": {"Arcade": 80},
        },
        {
            "_id": "2",
            "username": "david",
            "total_score": 150,
            "scores": {"Arcade": 120},
        },
    ]

    with patch(
        "src.services.user_service.UserService.get_all_users", return_value=mock_users
    ):
        res = UserService.get_top_users("Arcade")

    assert len(res) == 2
    assert res[0]["username"] == "david"
    assert res[0]["score"] == 120


def test_update_user_scores_by_username() -> None:
    with patch(
        "src.services.user_service.UserDAO.update_one_by_username",
        return_value=DummyUpdateResult(1),
    ):
        res = UserService.update_user_scores_by_username(
            "alice", {"scores": {"General": 200}, "total_score": 200}
        )

    assert isinstance(res, DummyUpdateResult)
    assert res.modified_count == 1


def test_delete_user_success() -> None:
    _id = ObjectId()

    with patch(
        "src.services.user_service.UserDAO.find_one_by_id",
        return_value={"_id": str(_id), "username": "alice"},
    ), patch(
        "src.services.user_service.UserDAO.delete_one_by_id",
        return_value=DummyDeleteResult(1),
    ):
        res = UserService.delete_user_by_id(_id)

    assert isinstance(res, DummyDeleteResult)
    assert res.deleted_count == 1


def test_delete_user_not_found() -> None:
    _id = ObjectId()

    with patch("src.services.user_service.UserDAO.find_one_by_id", return_value=None):
        with pytest.raises(NotFoundAPIError):
            UserService.delete_user_by_id(_id)
