import pytest
from pydantic import ValidationError

from src.models.flag_model import FlagModel


def test_flag_model_valid() -> None:
    flag = FlagModel(name="Argentina", image="arg.png")
    assert flag.name == "Argentina"
    assert flag.image == "arg.png"


def test_flag_model_strip_whitespace() -> None:
    flag = FlagModel(name="  Argentina  ", image="  arg.png  ")
    assert flag.name == "Argentina"
    assert flag.image == "arg.png"


def test_flag_model_invalid_empty_name() -> None:
    with pytest.raises(ValidationError):
        FlagModel(name="", image="arg.png")


def test_flag_model_invalid_empty_image() -> None:
    with pytest.raises(ValidationError):
        FlagModel(name="Argentina", image="")
