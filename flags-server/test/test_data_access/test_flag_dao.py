from typing import Any

from src.data_access.flag_dao import FlagDAO


def test_insert_and_find(unique_flag: dict[str, Any]) -> None:
    res = FlagDAO.insert_one(unique_flag)
    assert res.inserted_id is not None

    flags = FlagDAO.find()
    assert len(flags) == 1
    assert flags[0]["name"] == unique_flag["name"]
    assert "_id" in flags[0]


def test_find_one_by_id(unique_flag: dict[str, Any]) -> None:
    inserted = FlagDAO.insert_one(unique_flag)
    _id = inserted.inserted_id

    found = FlagDAO.find_one_by_id(_id)
    assert found is not None
    assert found["name"] == unique_flag["name"]
    assert str(_id) == found["_id"]


def test_find_one_by_name(unique_flag: dict[str, Any]) -> None:
    FlagDAO.insert_one(unique_flag)

    found = FlagDAO.find_one_by_name(unique_flag["name"])
    assert found is not None
    assert found["name"] == unique_flag["name"]

    found_ci = FlagDAO.find_one_by_name(unique_flag["name"].lower())
    assert found_ci is not None
    assert found_ci["name"] == unique_flag["name"]


def test_find_random() -> None:
    for i in range(5):
        FlagDAO.insert_one({"name": f"Flag {i}", "image": "img.png"})

    random_flags = FlagDAO.find_random(3)
    assert len(random_flags) == 3
    for flag in random_flags:
        assert "name" in flag
        assert "_id" in flag


def test_delete_one_by_id(unique_flag: dict[str, Any]) -> None:
    inserted = FlagDAO.insert_one(unique_flag)
    _id = inserted.inserted_id

    delete_result = FlagDAO.delete_one_by_id(_id)
    assert delete_result.deleted_count == 1

    not_found = FlagDAO.find_one_by_id(_id)
    assert not_found is None


def test_parse_flag_and_parse_flags(unique_flag: dict[str, Any]) -> None:
    inserted = FlagDAO.insert_one(unique_flag)
    doc = FlagDAO.find_one_by_id(inserted.inserted_id)

    parsed = FlagDAO.parse_flag(doc)
    assert parsed["_id"] == str(inserted.inserted_id)
    assert parsed["name"] == unique_flag["name"]

    parsed_list = FlagDAO.parse_flags([doc])
    assert isinstance(parsed_list, list)
    assert parsed_list[0]["name"] == unique_flag["name"]
