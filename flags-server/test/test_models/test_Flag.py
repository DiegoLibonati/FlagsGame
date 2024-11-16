from bson import ObjectId

import re

import pytest

from src.models.Flag import Flag

from test.conftest import TEST_FLAG_MOCK
from test.conftest import NOT_FOUND_ID_FLAG
from test.conftest import WRONG_ID_FLAG

def test_flag_model(flag_model: Flag) -> None:
    
    assert not flag_model.id 
    assert flag_model.name == TEST_FLAG_MOCK.get("name")
    assert flag_model.image == TEST_FLAG_MOCK.get("image")

    assert not re.search(r'\s', flag_model.name)
    assert not re.search(r'\s', flag_model.image)

def test_flag_is_valid(flag_model: Flag) -> None:
    assert flag_model.is_valid

def test_flag_is_not_valid(not_valid_flag_model: Flag) -> None:
    assert not not_valid_flag_model.is_valid

def test_set_flag_id(flag_model: Flag) -> None:
    flag_model.set_flag_id(id=NOT_FOUND_ID_FLAG)

    assert flag_model.id
    assert isinstance(flag_model.id, ObjectId)

def test_wrong_set_flag_id(flag_model: Flag) -> None:
    with pytest.raises(ValueError) as exc_info:
        flag_model.set_flag_id(id=WRONG_ID_FLAG)

    assert str(exc_info.value) == f"Invalid ID format: {WRONG_ID_FLAG}."

def test_flag_to_dict(flag_model: Flag) -> None:
    flag_dict = flag_model.to_dict()

    assert isinstance(flag_dict, dict)
    assert flag_dict.get("name") == flag_model.name
    assert flag_dict.get("image") == flag_model.image
