from functools import reduce
from bson import ObjectId

import pytest

from src.models.Encrypt import Encrypt
from src.data_access.users_repository import UserRepository


@pytest.mark.usefixtures("mongo_test_db")
def test_get_all_users(user_repository: UserRepository) -> None:
    users = user_repository.get_all_users()

    assert isinstance(users, list)

    if users:
        first_user = users[0]

        assert first_user
        assert first_user.get("_id")
        assert first_user.get("username")
        assert first_user.get("scores")
        assert first_user.get("total_score")
        assert first_user.get("password")

@pytest.mark.usefixtures("mongo_test_db")
def test_insert_and_get_and_delete_user_by_id(user_repository: UserRepository, test_user: dict[str, str]) -> None:
    username = test_user.get("username")
    encrypt = Encrypt(password=test_user.get("password"))
    scores = test_user.get("scores")
    total_score = test_user.get("total_score")

    user_id = user_repository.insert_user(user={
        "username": username, 
        "password": encrypt.password_hashed, 
        "scores": scores,
        "total_score": total_score
    })

    assert user_id
    assert isinstance(user_id, str)

    user_id = ObjectId(user_id)

    assert isinstance(user_id, ObjectId)

    user = user_repository.get_user_by_id(user_id=user_id)

    assert user
    assert ObjectId(user.get("_id")) == user_id
    assert user.get("username") == username
    assert user.get("scores") == scores
    assert user.get("total_score") == total_score
    assert encrypt.valid_password(pwhash=user.get("password"))

    user_repository.delete_user_by_id(user_id=user_id)

    user = user_repository.get_user_by_id(user_id=user_id)

    assert not user

@pytest.mark.usefixtures("mongo_test_db")
def test_insert_and_get_and_delete_user_by_username(user_repository: UserRepository, test_user: dict[str, str]) -> None:
    username = test_user.get("username")
    encrypt = Encrypt(password=test_user.get("password"))
    scores = test_user.get("scores")
    total_score = test_user.get("total_score")

    user_id = user_repository.insert_user(user={
        "username": username, 
        "password": encrypt.password_hashed, 
        "scores": scores,
        "total_score": total_score
    })

    assert user_id
    assert isinstance(user_id, str)

    user_id = ObjectId(user_id)

    assert isinstance(user_id, ObjectId)

    user = user_repository.get_user_by_username(username=username)

    assert user
    assert ObjectId(user.get("_id")) == user_id
    assert user.get("username") == username
    assert user.get("scores") == scores
    assert user.get("total_score") == total_score
    assert encrypt.valid_password(pwhash=user.get("password"))

    user_repository.delete_user_by_id(user_id=user_id)

    user = user_repository.get_user_by_username(username=username)

    assert not user

@pytest.mark.usefixtures("mongo_test_db")
def test_update_existing_mode_of_user(user_repository: UserRepository, test_user: dict[str, str]) -> None:
    username = test_user.get("username")
    encrypt = Encrypt(password=test_user.get("password"))
    scores = test_user.get("scores")
    total_score = test_user.get("total_score")

    user_id = user_repository.insert_user(user={
        "username": username, 
        "password": encrypt.password_hashed, 
        "scores": scores,
        "total_score": total_score
    })

    user = user_repository.get_user_by_username(username=username)

    user_id = ObjectId(user_id)

    assert user
    assert ObjectId(user.get("_id")) == user_id
    assert user.get("username") == username
    assert user.get("scores") == scores
    assert user.get("total_score") == total_score
    assert encrypt.valid_password(pwhash=user.get("password"))

    mode_name = "normal"
    mode_score = 100

    scores = {"general": mode_score, mode_name: mode_score}

    values = {"scores": scores, "total_score": reduce(lambda a, b: a+b, scores.values()) - scores["general"] }

    user_repository.update_user_by_username(username=username, values=values)

    user = user_repository.get_user_by_username(username=username)

    assert ObjectId(user.get("_id")) == user_id
    assert user.get("username") == username
    assert user.get("scores") == {"general": mode_score, "normal": mode_score}
    assert user.get("total_score") == reduce(lambda a, b: a+b, user["scores"].values()) - user["scores"]["general"]
    assert encrypt.valid_password(pwhash=user.get("password"))

    user_repository.delete_user_by_id(user_id=user_id)

    user = user_repository.get_user_by_username(username=username)

    assert not user

@pytest.mark.usefixtures("mongo_test_db")
def test_update_not_existing_mode_of_user(user_repository: UserRepository, test_user: dict[str, str]) -> None:
    username = test_user.get("username")
    encrypt = Encrypt(password=test_user.get("password"))
    scores = test_user.get("scores")
    total_score = test_user.get("total_score")

    user_id = user_repository.insert_user(user={
        "username": username, 
        "password": encrypt.password_hashed, 
        "scores": scores,
        "total_score": total_score
    })

    user = user_repository.get_user_by_username(username=username)

    user_id = ObjectId(user_id)

    assert user
    assert ObjectId(user.get("_id")) == user_id
    assert user.get("username") == username
    assert user.get("scores") == scores
    assert user.get("total_score") == total_score
    assert encrypt.valid_password(pwhash=user.get("password"))

    mode_name = "hard"
    mode_score = 100

    scores = {"general": mode_score + 25, "normal": 25, mode_name: mode_score}
    
    values = {"scores": scores, "total_score": reduce(lambda a, b: a+b, scores.values()) - scores["general"] }

    user_repository.update_user_by_username(username=username, values=values)

    user = user_repository.get_user_by_username(username=username)

    assert user
    assert ObjectId(user.get("_id")) == user_id
    assert user.get("username") == username
    assert user.get("scores") == {"general": mode_score + 25, "normal": 25, "hard": mode_score}
    assert user.get("total_score") == reduce(lambda a, b: a+b, user["scores"].values()) - user["scores"]["general"]
    assert encrypt.valid_password(pwhash=user.get("password"))

    user_repository.delete_user_by_id(user_id=user_id)

    user = user_repository.get_user_by_username(username=username)

    assert not user