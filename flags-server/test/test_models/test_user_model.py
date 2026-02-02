import pytest
from pydantic import ValidationError

from src.models.user_model import UserModel


class TestUserModelCreation:
    def test_create_valid_user(self) -> None:
        user = UserModel(
            username="testuser",
            password="testpassword",
            scores={"General": 100, "Normal": 100},
            total_score=100,
        )

        assert user.username == "testuser"
        assert user.password == "testpassword"
        assert user.scores == {"General": 100, "Normal": 100}
        assert user.total_score == 100

    def test_model_dump_returns_dict(self) -> None:
        user = UserModel(
            username="player1",
            password="secret123",
            scores={"General": 200},
            total_score=200,
        )

        result = user.model_dump()

        assert isinstance(result, dict)
        assert result == {
            "username": "player1",
            "password": "secret123",
            "scores": {"General": 200},
            "total_score": 200,
        }


class TestUserModelRequiredFields:
    def test_username_is_required(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            UserModel(password="pass", scores={}, total_score=0)

        errors = exc_info.value.errors()
        assert any(e["loc"] == ("username",) for e in errors)

    def test_password_is_required(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            UserModel(username="user", scores={}, total_score=0)

        errors = exc_info.value.errors()
        assert any(e["loc"] == ("password",) for e in errors)

    def test_scores_is_required(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            UserModel(username="user", password="pass", total_score=0)

        errors = exc_info.value.errors()
        assert any(e["loc"] == ("scores",) for e in errors)

    def test_total_score_is_required(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            UserModel(username="user", password="pass", scores={})

        errors = exc_info.value.errors()
        assert any(e["loc"] == ("total_score",) for e in errors)

    def test_empty_model_fails(self) -> None:
        with pytest.raises(ValidationError):
            UserModel()


class TestUserModelMinLength:
    def test_username_cannot_be_empty(self) -> None:
        with pytest.raises(ValidationError):
            UserModel(username="", password="pass", scores={}, total_score=0)

    def test_password_cannot_be_empty(self) -> None:
        with pytest.raises(ValidationError):
            UserModel(username="user", password="", scores={}, total_score=0)

    def test_single_character_is_valid(self) -> None:
        user = UserModel(username="A", password="B", scores={}, total_score=0)

        assert user.username == "A"
        assert user.password == "B"


class TestUserModelStripWhitespace:
    def test_username_strips_whitespace(self) -> None:
        user = UserModel(
            username="  testuser  ", password="pass", scores={}, total_score=0
        )

        assert user.username == "testuser"

    def test_password_strips_whitespace(self) -> None:
        user = UserModel(
            username="user", password="  secret  ", scores={}, total_score=0
        )

        assert user.password == "secret"

    def test_only_whitespace_username_fails(self) -> None:
        with pytest.raises(ValidationError):
            UserModel(username="   ", password="pass", scores={}, total_score=0)

    def test_only_whitespace_password_fails(self) -> None:
        with pytest.raises(ValidationError):
            UserModel(username="user", password="   ", scores={}, total_score=0)


class TestUserModelNoneValues:
    def test_username_none_fails(self) -> None:
        with pytest.raises(ValidationError):
            UserModel(username=None, password="pass", scores={}, total_score=0)

    def test_password_none_fails(self) -> None:
        with pytest.raises(ValidationError):
            UserModel(username="user", password=None, scores={}, total_score=0)

    def test_scores_none_fails(self) -> None:
        with pytest.raises(ValidationError):
            UserModel(username="user", password="pass", scores=None, total_score=0)

    def test_total_score_none_fails(self) -> None:
        with pytest.raises(ValidationError):
            UserModel(username="user", password="pass", scores={}, total_score=None)


class TestUserModelScoresField:
    def test_scores_accepts_empty_dict(self) -> None:
        user = UserModel(username="user", password="pass", scores={}, total_score=0)

        assert user.scores == {}

    def test_scores_accepts_single_entry(self) -> None:
        user = UserModel(
            username="user", password="pass", scores={"General": 100}, total_score=100
        )

        assert user.scores == {"General": 100}

    def test_scores_accepts_multiple_entries(self) -> None:
        scores = {"General": 300, "Normal": 100, "Hard": 200}
        user = UserModel(
            username="user", password="pass", scores=scores, total_score=300
        )

        assert user.scores == scores

    def test_scores_values_must_be_int(self) -> None:
        with pytest.raises(ValidationError):
            UserModel(
                username="user",
                password="pass",
                scores={"General": "one hundred"},
                total_score=0,
            )


class TestUserModelTotalScoreField:
    def test_total_score_accepts_zero(self) -> None:
        user = UserModel(username="user", password="pass", scores={}, total_score=0)

        assert user.total_score == 0

    def test_total_score_accepts_positive(self) -> None:
        user = UserModel(username="user", password="pass", scores={}, total_score=1000)

        assert user.total_score == 1000

    def test_total_score_accepts_negative(self) -> None:
        user = UserModel(username="user", password="pass", scores={}, total_score=-50)

        assert user.total_score == -50

    def test_total_score_string_fails(self) -> None:
        with pytest.raises(ValidationError):
            UserModel(
                username="user", password="pass", scores={}, total_score="hundred"
            )


class TestUserModelSerialization:
    def test_model_to_json(self) -> None:
        user = UserModel(
            username="player",
            password="secret",
            scores={"General": 500},
            total_score=500,
        )

        json_str = user.model_dump_json()

        assert "player" in json_str
        assert "secret" in json_str
        assert "500" in json_str

    def test_model_from_dict(self) -> None:
        data = {
            "username": "newplayer",
            "password": "newpass",
            "scores": {"General": 0},
            "total_score": 0,
        }

        user = UserModel(**data)

        assert user.username == "newplayer"
        assert user.total_score == 0

    def test_model_ignores_extra_fields(self) -> None:
        user = UserModel(
            username="user",
            password="pass",
            scores={},
            total_score=0,
            extra_field="ignored",
        )

        assert user.username == "user"
        assert not hasattr(user, "extra_field")
