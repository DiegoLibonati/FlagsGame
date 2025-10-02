from typing import Any

from src.data_access.user_dao import UserDAO


def test_insert_and_find(unique_user: dict[str, Any]) -> None:
    res = UserDAO.insert_one(unique_user)
    assert res.inserted_id is not None

    users = UserDAO.find()
    assert len(users) == 1
    assert users[0]["username"] == unique_user["username"]
    assert "_id" in users[0]


def test_find_one_by_id(unique_user: dict[str, Any]) -> None:
    inserted = UserDAO.insert_one(unique_user)
    _id = inserted.inserted_id

    found = UserDAO.find_one_by_id(_id)
    assert found is not None
    assert found["username"] == unique_user["username"]
    assert str(_id) == found["_id"]


def test_find_one_by_username(unique_user: dict[str, Any]) -> None:
    UserDAO.insert_one(unique_user)

    found = UserDAO.find_one_by_username(unique_user["username"])
    assert found is not None
    assert found["username"] == unique_user["username"]


def test_update_one_by_username(unique_user: dict[str, Any]) -> None:
    UserDAO.insert_one(unique_user)

    new_values = {"total_score": 999}
    update_result = UserDAO.update_one_by_username(unique_user["username"], new_values)
    assert update_result.modified_count == 1

    updated = UserDAO.find_one_by_username(unique_user["username"])
    assert updated["total_score"] == 999


def test_delete_one_by_id(unique_user: dict[str, Any]) -> None:
    inserted = UserDAO.insert_one(unique_user)
    _id = inserted.inserted_id

    delete_result = UserDAO.delete_one_by_id(_id)
    assert delete_result.deleted_count == 1

    not_found = UserDAO.find_one_by_id(_id)
    assert not_found is None


def test_parse_user_and_parse_users(unique_user: dict[str, Any]) -> None:
    inserted = UserDAO.insert_one(unique_user)
    doc = UserDAO.find_one_by_id(inserted.inserted_id)

    parsed = UserDAO.parse_user(doc)
    assert parsed["_id"] == str(inserted.inserted_id)
    assert parsed["username"] == unique_user["username"]

    parsed_list = UserDAO.parse_users([doc])
    assert isinstance(parsed_list, list)
    assert parsed_list[0]["username"] == unique_user["username"]
