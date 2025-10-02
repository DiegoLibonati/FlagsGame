import pytest
from pydantic import ValidationError

from src.models.user_model import UserModel


def test_user_model_valid() -> None:
    user = UserModel(
        username="player1",
        password="securepass",
        scores={"General": 100, "Arcade": 50},
        total_score=150,
    )
    assert user.username == "player1"
    assert user.password == "securepass"
    assert isinstance(user.scores, dict)
    assert user.scores["General"] == 100
    assert user.total_score == 150


def test_user_model_strip_whitespace() -> None:
    user = UserModel(
        username="  player1  ",
        password="  pass123  ",
        scores={"General": 200},
        total_score=200,
    )
    assert user.username == "player1"
    assert user.password == "pass123"


def test_user_model_invalid_empty_username() -> None:
    with pytest.raises(ValidationError):
        UserModel(username="", password="pass", scores={"General": 10}, total_score=10)


def test_user_model_invalid_empty_password() -> None:
    with pytest.raises(ValidationError):
        UserModel(
            username="player", password="", scores={"General": 10}, total_score=10
        )


def test_user_model_invalid_scores_type() -> None:
    with pytest.raises(ValidationError):
        UserModel(
            username="player", password="pass", scores="not_a_dict", total_score=10
        )


def test_user_model_invalid_total_score_type() -> None:
    with pytest.raises(ValidationError):
        UserModel(
            username="player",
            password="pass",
            scores={"General": 10},
            total_score="abc",
        )
