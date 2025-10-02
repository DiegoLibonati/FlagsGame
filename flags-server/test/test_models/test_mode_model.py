import pytest
from pydantic import ValidationError

from src.models.mode_model import ModeModel


def test_mode_model_valid() -> None:
    mode = ModeModel(
        name="Arcade",
        description="Fast-paced mode",
        multiplier=10,
        timeleft=60,
    )
    assert mode.name == "Arcade"
    assert mode.description == "Fast-paced mode"
    assert mode.multiplier == 10
    assert mode.timeleft == 60


def test_mode_model_strip_whitespace() -> None:
    mode = ModeModel(
        name="  Arcade  ",
        description="  Fast-paced mode  ",
        multiplier=5,
        timeleft=30,
    )
    assert mode.name == "Arcade"
    assert mode.description == "Fast-paced mode"


def test_mode_model_invalid_empty_name() -> None:
    with pytest.raises(ValidationError):
        ModeModel(name="", description="desc", multiplier=1, timeleft=10)


def test_mode_model_invalid_empty_description() -> None:
    with pytest.raises(ValidationError):
        ModeModel(name="Arcade", description="", multiplier=1, timeleft=10)


def test_mode_model_invalid_non_integer_multiplier() -> None:
    with pytest.raises(ValidationError):
        ModeModel(name="Arcade", description="desc", multiplier="abc", timeleft=10)


def test_mode_model_invalid_non_integer_timeleft() -> None:
    with pytest.raises(ValidationError):
        ModeModel(name="Arcade", description="desc", multiplier=1, timeleft="abc")
