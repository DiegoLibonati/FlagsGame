import logging

from typing import Any

import pytest

from src.models.User import User
from src.models.UserManager import UserManager

from test.constants import NOT_FOUND_ID_USER


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def test_init_user_manager(user_manager_model: UserManager, test_users: dict[str, Any]) -> None:
    assert user_manager_model
    assert not user_manager_model.users
    assert user_manager_model.initializer(**test_users[0])

def test_add_user(user_manager_model: UserManager, user_model: User) -> None:
    user_manager_model.add_user(user=user_model)

    assert user_manager_model.users
    assert user_model in user_manager_model.users

def test_add_user_with_wrong_user(user_manager_model: UserManager) -> None:
    with pytest.raises(TypeError) as exc_info:
        user_manager_model.add_user(user={"pepe": "123"})

    assert str(exc_info.value) == "You must enter a valid user in order to add it."

def test_add_users(user_manager_model: UserManager, test_users: dict[str, str]) -> None:
    user_manager_model.add_users(users=test_users)

    assert user_manager_model.users
    
    for user in user_manager_model.users:
        if str(user.id) == NOT_FOUND_ID_USER: continue
        assert {**user.to_dict(), "password": "1234"} in test_users

def test_add_users_with_wrong_users(user_manager_model: UserManager) -> None:
    with pytest.raises(TypeError) as exc_info:
        user_manager_model.add_users(users=[])

    assert str(exc_info.value) == "You must enter a valid users to add its."

def test_parse_users(user_manager_model: UserManager) -> None:
    parsed_users = user_manager_model.parse_items()

    assert isinstance(parsed_users, list)

    for user in parsed_users:
        assert isinstance(user, dict)
        assert user.get("_id")
        assert user.get("username")
        assert user.get("scores")
        assert user.get("total_score")

def test_get_users_top_ten(user_manager_model: UserManager) -> None:
    mode_name="normal"

    top_ten = user_manager_model.get_users_top_ten(mode_name=mode_name)

    if len(top_ten) >= 2:
        first_user = top_ten[0]
        second_user = top_ten[1]

        assert first_user.get("score") >= second_user.get("score")

    assert len(top_ten) >= 0 and len(top_ten) <= 10



