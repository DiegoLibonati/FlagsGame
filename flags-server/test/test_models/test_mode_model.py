import pytest
from pydantic import ValidationError

from src.models.mode_model import ModeModel


class TestModeModelCreation:
    def test_create_valid_mode(self) -> None:
        mode = ModeModel(
            name="Normal",
            description="Normal mode description",
            multiplier=10,
            timeleft=90,
        )

        assert mode.name == "Normal"
        assert mode.description == "Normal mode description"
        assert mode.multiplier == 10
        assert mode.timeleft == 90

    def test_model_dump_returns_dict(self) -> None:
        mode = ModeModel(
            name="Hard", description="Hard mode", multiplier=100, timeleft=60
        )

        result = mode.model_dump()

        assert isinstance(result, dict)
        assert result == {
            "name": "Hard",
            "description": "Hard mode",
            "multiplier": 100,
            "timeleft": 60,
        }


class TestModeModelRequiredFields:
    def test_name_is_required(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            ModeModel(description="Desc", multiplier=10, timeleft=90)

        errors = exc_info.value.errors()
        assert any(e["loc"] == ("name",) for e in errors)

    def test_description_is_required(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            ModeModel(name="Test", multiplier=10, timeleft=90)

        errors = exc_info.value.errors()
        assert any(e["loc"] == ("description",) for e in errors)

    def test_multiplier_is_required(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            ModeModel(name="Test", description="Desc", timeleft=90)

        errors = exc_info.value.errors()
        assert any(e["loc"] == ("multiplier",) for e in errors)

    def test_timeleft_is_required(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            ModeModel(name="Test", description="Desc", multiplier=10)

        errors = exc_info.value.errors()
        assert any(e["loc"] == ("timeleft",) for e in errors)

    def test_empty_model_fails(self) -> None:
        with pytest.raises(ValidationError):
            ModeModel()


class TestModeModelMinLength:
    def test_name_cannot_be_empty(self) -> None:
        with pytest.raises(ValidationError):
            ModeModel(name="", description="Desc", multiplier=10, timeleft=90)

    def test_description_cannot_be_empty(self) -> None:
        with pytest.raises(ValidationError):
            ModeModel(name="Test", description="", multiplier=10, timeleft=90)

    def test_single_character_is_valid(self) -> None:
        mode = ModeModel(name="A", description="B", multiplier=10, timeleft=90)

        assert mode.name == "A"
        assert mode.description == "B"


class TestModeModelStripWhitespace:
    def test_name_strips_whitespace(self) -> None:
        mode = ModeModel(
            name="  Normal  ", description="Desc", multiplier=10, timeleft=90
        )

        assert mode.name == "Normal"

    def test_description_strips_whitespace(self) -> None:
        mode = ModeModel(
            name="Test", description="  Description  ", multiplier=10, timeleft=90
        )

        assert mode.description == "Description"

    def test_only_whitespace_name_fails(self) -> None:
        with pytest.raises(ValidationError):
            ModeModel(name="   ", description="Desc", multiplier=10, timeleft=90)

    def test_only_whitespace_description_fails(self) -> None:
        with pytest.raises(ValidationError):
            ModeModel(name="Test", description="   ", multiplier=10, timeleft=90)


class TestModeModelNoneValues:
    def test_name_none_fails(self) -> None:
        with pytest.raises(ValidationError):
            ModeModel(name=None, description="Desc", multiplier=10, timeleft=90)

    def test_description_none_fails(self) -> None:
        with pytest.raises(ValidationError):
            ModeModel(name="Test", description=None, multiplier=10, timeleft=90)

    def test_multiplier_none_fails(self) -> None:
        with pytest.raises(ValidationError):
            ModeModel(name="Test", description="Desc", multiplier=None, timeleft=90)

    def test_timeleft_none_fails(self) -> None:
        with pytest.raises(ValidationError):
            ModeModel(name="Test", description="Desc", multiplier=10, timeleft=None)


class TestModeModelIntegerFields:
    def test_multiplier_accepts_zero(self) -> None:
        mode = ModeModel(name="Test", description="Desc", multiplier=0, timeleft=90)

        assert mode.multiplier == 0

    def test_timeleft_accepts_zero(self) -> None:
        mode = ModeModel(name="Test", description="Desc", multiplier=10, timeleft=0)

        assert mode.timeleft == 0

    def test_multiplier_accepts_negative(self) -> None:
        mode = ModeModel(name="Test", description="Desc", multiplier=-10, timeleft=90)

        assert mode.multiplier == -10

    def test_timeleft_accepts_negative(self) -> None:
        mode = ModeModel(name="Test", description="Desc", multiplier=10, timeleft=-30)

        assert mode.timeleft == -30

    def test_multiplier_accepts_large_number(self) -> None:
        mode = ModeModel(
            name="Test", description="Desc", multiplier=1000000, timeleft=90
        )

        assert mode.multiplier == 1000000

    def test_multiplier_string_fails(self) -> None:
        with pytest.raises(ValidationError):
            ModeModel(name="Test", description="Desc", multiplier="ten", timeleft=90)

    def test_timeleft_string_fails(self) -> None:
        with pytest.raises(ValidationError):
            ModeModel(name="Test", description="Desc", multiplier=10, timeleft="ninety")


class TestModeModelSerialization:
    def test_model_to_json(self) -> None:
        mode = ModeModel(
            name="Hardcore", description="Hardcore mode", multiplier=1000, timeleft=30
        )

        json_str = mode.model_dump_json()

        assert "Hardcore" in json_str
        assert "1000" in json_str
        assert "30" in json_str

    def test_model_from_dict(self) -> None:
        data = {
            "name": "Custom",
            "description": "Custom mode",
            "multiplier": 50,
            "timeleft": 45,
        }

        mode = ModeModel(**data)

        assert mode.name == "Custom"
        assert mode.multiplier == 50

    def test_model_ignores_extra_fields(self) -> None:
        mode = ModeModel(
            name="Test",
            description="Desc",
            multiplier=10,
            timeleft=90,
            extra_field="ignored",
        )

        assert mode.name == "Test"
        assert not hasattr(mode, "extra_field")
