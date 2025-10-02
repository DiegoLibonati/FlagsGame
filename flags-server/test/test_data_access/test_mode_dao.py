from typing import Any

from src.data_access.mode_dao import ModeDAO


def test_insert_and_find(unique_mode: dict[str, Any]) -> None:
    res = ModeDAO.insert_one(unique_mode)
    assert res.inserted_id is not None

    modes = ModeDAO.find()
    assert len(modes) == 1
    assert modes[0]["name"] == unique_mode["name"]
    assert "_id" in modes[0]


def test_find_one_by_id(unique_mode: dict[str, Any]) -> None:
    inserted = ModeDAO.insert_one(unique_mode)
    _id = inserted.inserted_id

    found = ModeDAO.find_one_by_id(_id)
    assert found is not None
    assert found["name"] == unique_mode["name"]
    assert str(_id) == found["_id"]


def test_find_one_by_name(unique_mode: dict[str, Any]) -> None:
    ModeDAO.insert_one(unique_mode)

    found = ModeDAO.find_one_by_name(unique_mode["name"])
    assert found is not None
    assert found["name"] == unique_mode["name"]

    found_ci = ModeDAO.find_one_by_name(unique_mode["name"].lower())
    assert found_ci is not None
    assert found_ci["name"] == unique_mode["name"]


def test_delete_one_by_id(unique_mode: dict[str, Any]) -> None:
    inserted = ModeDAO.insert_one(unique_mode)
    _id = inserted.inserted_id

    delete_result = ModeDAO.delete_one_by_id(_id)
    assert delete_result.deleted_count == 1

    not_found = ModeDAO.find_one_by_id(_id)
    assert not_found is None


def test_parse_mode_and_parse_modes(unique_mode: dict[str, Any]) -> None:
    inserted = ModeDAO.insert_one(unique_mode)
    doc = ModeDAO.find_one_by_id(inserted.inserted_id)

    parsed = ModeDAO.parse_mode(doc)
    assert parsed["_id"] == str(inserted.inserted_id)
    assert parsed["name"] == unique_mode["name"]

    parsed_list = ModeDAO.parse_modes([doc])
    assert isinstance(parsed_list, list)
    assert parsed_list[0]["name"] == unique_mode["name"]
