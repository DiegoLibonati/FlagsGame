from bson import ObjectId

import pytest

from src.models.Encrypt import Encrypt
from src.models.User import User
from src.data_access.users_repository import UserRepository


@pytest.mark.usefixtures("mongo_test_db", "app_context")
def test_get_all_users(user_repository: UserRepository) -> None:
    users = user_repository.get_all_users()

    assert isinstance(users, list)

    if users:
        first_user = users[0]

        _id = first_user.get("_id")
        username = first_user.get("username")
        scores = first_user.get("scores")
        total_score = first_user.get("total_score")
        password = first_user.get("password")

        user = User(**first_user)

        assert user.id == _id
        assert user.username == username
        assert user.scores == scores
        assert user.total_score == total_score
        assert user.password == password

@pytest.mark.usefixtures("mongo_test_db", "app_context")
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
    user = User(**user)

    assert user
    assert user.id == user_id
    assert user.username == username
    assert user.scores == scores
    assert user.total_score == total_score
    assert encrypt.valid_password(pwhash=user.password)

    user_repository.delete_user_by_id(user_id=user_id)

    user = user_repository.get_user_by_id(user_id=user_id)

    assert not user


@pytest.mark.usefixtures("mongo_test_db", "app_context")
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
    user = User(**user)

    assert user
    assert user.id == user_id
    assert user.username == username
    assert user.scores == scores
    assert user.total_score == total_score
    assert encrypt.valid_password(pwhash=user.password)

    user_repository.delete_user_by_id(user_id=user_id)

    user = user_repository.get_user_by_username(username=username)

    assert not user


@pytest.mark.usefixtures("mongo_test_db", "app_context")
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
    user = User(**user)

    user_id = ObjectId(user_id)

    assert user
    assert user.id == user_id
    assert user.username == username
    assert user.scores == scores
    assert user.total_score == total_score
    assert encrypt.valid_password(pwhash=user.password)

    mode_name = "normal"
    mode_score = 100

    user.update_scores(mode_name=mode_name, score=mode_score)

    values = {"scores": user.scores, "total_score": user.total_score}

    user_repository.update_user_by_username(username=username, values=values)

    user = user_repository.get_user_by_username(username=username)
    user = User(**user)

    assert user.id == user_id
    assert user.username == username
    assert user.scores == {"general": mode_score, "normal": mode_score}
    assert user.total_score == mode_score
    assert encrypt.valid_password(pwhash=user.password)

    user_repository.delete_user_by_id(user_id=user_id)

    user = user_repository.get_user_by_username(username=username)

    assert not user


@pytest.mark.usefixtures("mongo_test_db", "app_context")
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
    user = User(**user)

    user_id = ObjectId(user_id)

    assert user
    assert user.id == user_id
    assert user.username == username
    assert user.scores == scores
    assert user.total_score == total_score
    assert encrypt.valid_password(pwhash=user.password)

    mode_name = "hard"
    mode_score = 100

    user.update_scores(mode_name=mode_name, score=mode_score)

    values = {"scores": user.scores, "total_score": user.total_score}

    user_repository.update_user_by_username(username=username, values=values)

    user = user_repository.get_user_by_username(username=username)
    user = User(**user)

    assert user.id == user_id
    assert user.username == username
    assert user.scores == {"general": mode_score + 25, "normal": 25, "hard": mode_score}
    assert user.total_score == mode_score + 25
    assert encrypt.valid_password(pwhash=user.password)

    user_repository.delete_user_by_id(user_id=user_id)

    user = user_repository.get_user_by_username(username=username)

    assert not user