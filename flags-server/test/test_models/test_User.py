from functools import reduce
from bson import ObjectId

from src.models.User import User

from test.constants import TEST_USER_MOCK


def test_user_model(user_model: User) -> None:
    _id = TEST_USER_MOCK.get("_id")
    username = TEST_USER_MOCK.get("username")
    password = TEST_USER_MOCK.get("password")
    scores = TEST_USER_MOCK.get("scores")
    total_score = TEST_USER_MOCK.get("total_score")


    assert user_model.id == ObjectId(_id)
    assert user_model.username == username
    assert user_model.password == password
    assert user_model.scores == scores
    assert user_model.total_score == total_score

def test_user_to_dict(user_model: User) -> None:
    user_dict = user_model.to_dict()

    assert isinstance(user_dict, dict)
    assert user_dict.get("_id") == str(user_model.id)
    assert user_dict.get("username") == user_model.username
    assert user_dict.get("scores") == user_model.scores
    assert user_dict.get("total_score") == user_model.total_score

def test_user_update_scores_with_existing_mode(user_model: User) -> None:
    mode_name = "normal"
    mode_score = 100

    user_model.update_scores(mode_name=mode_name, score=mode_score)

    assert user_model.scores.get(mode_name) == mode_score
    assert user_model.total_score == reduce(lambda a, b: a+b, user_model.scores.values()) - user_model.scores.get("general")

def test_user_update_scores_without_existing_mode(user_model: User) -> None:
    mode_name = "hell"
    mode_score = 200

    user_model.update_scores(mode_name=mode_name, score=mode_score)

    assert user_model.scores.get(mode_name) == mode_score
    assert user_model.total_score == reduce(lambda a, b: a+b, user_model.scores.values()) - user_model.scores.get("general")
