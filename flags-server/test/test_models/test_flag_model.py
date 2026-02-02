import pytest
from pydantic import ValidationError

from src.models.flag_model import FlagModel


class TestFlagModelCreation:
    def test_create_valid_flag(self) -> None:
        flag = FlagModel(name="Argentina", image="https://example.com/argentina.png")

        assert flag.name == "Argentina"
        assert flag.image == "https://example.com/argentina.png"

    def test_model_dump_returns_dict(self) -> None:
        flag = FlagModel(name="Brasil", image="https://example.com/brasil.png")

        result = flag.model_dump()

        assert isinstance(result, dict)
        assert result == {"name": "Brasil", "image": "https://example.com/brasil.png"}


class TestFlagModelRequiredFields:
    def test_name_is_required(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            FlagModel(image="https://example.com/test.png")

        errors = exc_info.value.errors()
        assert any(e["loc"] == ("name",) for e in errors)

    def test_image_is_required(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            FlagModel(name="Test")

        errors = exc_info.value.errors()
        assert any(e["loc"] == ("image",) for e in errors)

    def test_empty_model_fails(self) -> None:
        with pytest.raises(ValidationError):
            FlagModel()


class TestFlagModelMinLength:
    def test_name_cannot_be_empty(self) -> None:
        with pytest.raises(ValidationError):
            FlagModel(name="", image="https://example.com/test.png")

    def test_image_cannot_be_empty(self) -> None:
        with pytest.raises(ValidationError):
            FlagModel(name="Test", image="")

    def test_single_character_is_valid(self) -> None:
        flag = FlagModel(name="A", image="B")

        assert flag.name == "A"
        assert flag.image == "B"


class TestFlagModelStripWhitespace:
    def test_name_strips_whitespace(self) -> None:
        flag = FlagModel(name="  Argentina  ", image="https://example.com/test.png")

        assert flag.name == "Argentina"

    def test_image_strips_whitespace(self) -> None:
        flag = FlagModel(name="Test", image="  https://example.com/test.png  ")

        assert flag.image == "https://example.com/test.png"

    def test_only_whitespace_name_fails(self) -> None:
        with pytest.raises(ValidationError):
            FlagModel(name="   ", image="https://example.com/test.png")

    def test_only_whitespace_image_fails(self) -> None:
        with pytest.raises(ValidationError):
            FlagModel(name="Test", image="   ")


class TestFlagModelNoneValues:
    def test_name_none_fails(self) -> None:
        with pytest.raises(ValidationError):
            FlagModel(name=None, image="https://example.com/test.png")

    def test_image_none_fails(self) -> None:
        with pytest.raises(ValidationError):
            FlagModel(name="Test", image=None)


class TestFlagModelSerialization:
    def test_model_to_json(self) -> None:
        flag = FlagModel(name="Chile", image="https://example.com/chile.png")

        json_str = flag.model_dump_json()

        assert "Chile" in json_str
        assert "https://example.com/chile.png" in json_str

    def test_model_from_dict(self) -> None:
        data = {"name": "Peru", "image": "https://example.com/peru.png"}

        flag = FlagModel(**data)

        assert flag.name == "Peru"
        assert flag.image == "https://example.com/peru.png"

    def test_model_ignores_extra_fields(self) -> None:
        flag = FlagModel(
            name="Test", image="https://example.com/test.png", extra_field="ignored"
        )

        assert flag.name == "Test"
        assert not hasattr(flag, "extra_field")
