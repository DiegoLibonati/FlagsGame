from bson import ObjectId

from flask import make_response
from flask import current_app
from flask import request
from flask import Response

from src.models.Encrypt import Encrypt
from src.models.User import User
from src.models.UserManager import UserManager
from src.models.ModeManager import ModeManager


def top_general() -> Response:
    users = current_app.user_repository.get_all_users()
    user_manager = UserManager()

    if users: user_manager.add_users(users=users)

    data = user_manager.get_users_top_ten(mode_name="general")

    return make_response({
        "message": "Successfully obtained the global top.",
        "data": data
    }, 200)


def add_or_modify() -> Response:
    method = request.method

    username = request.json.get('username', "").strip()
    password = request.json.get('password', "").strip()
    score_actual = request.json.get('score')
    mode_name = request.json.get('mode_name', "").strip().lower()

    if not username or not password or not mode_name:
        return make_response({
            "message": "The data entered are not valid.",
            "data": None
        }, 400)
    
    modes = current_app.mode_repository.get_all_modes()

    mode_manager = ModeManager()
    if modes: mode_manager.add_modes(modes=modes)
    
    modes_names = mode_manager.get_modes_names()

    if not mode_name in modes_names:
        return make_response({
            "message": "The mode entered does not exist in the database.",
            "data": None
        }, 404)

    user = current_app.user_repository.get_user_by_username(username=username) 

    # NOTE: PUT

    if method == "PUT":
        if not user:
            return make_response({
                "message": "No valid user was found based on the data entered.",
                "data": None
            }, 404)
        
        user = User(**user)
        
        if not Encrypt(password=password).valid_password(pwhash=user.password):
            return make_response({
                "message": "Password do not match with that username.",
                "data": None
            }, 400)
        
        user.update_scores(mode_name=mode_name, score=score_actual)

        current_app.user_repository.update_user_by_username(username=username, values={"scores": user.scores, "total_score": user.total_score})

        return make_response({
            "message": "User successfully updated.",
            "data": user.to_dict()
        }, 201)

    # NOTE: POST

    if method == "POST":

        if not user:
            scores = {"general": score_actual, mode_name: score_actual}

            current_app.user_repository.insert_user(user={'username': username, 'password': Encrypt(password=password).password_hashed, 'scores': scores, 'total_score': scores.get("general")})

            user = current_app.user_repository.get_user_by_username(username=username) 

            return make_response({
                "message":"User successfully added.",
                "data": User(**user).to_dict()
            }, 201)
        
        if user:
            return make_response({
                "message": "There is a user with that username.",
                "data": User(**user).to_dict()
            }, 400)
    
    return make_response({
        "message": "No action was taken.",
        "data": None
    }, 400)


def delete_user(id: str) -> Response:
    try:
        object_id = ObjectId(id)
        document = current_app.user_repository.get_user_by_id(user_id=object_id)

        if not document: 
            return make_response({
                "message": f"No user found with id: {id}.",
                "data": None
            }, 404)
        
        user = User(**document)

        current_app.user_repository.delete_user_by_id(user_id=user.id)

        return make_response({
            "message": f"User with id: {id} was deleted.",
            "data": user.to_dict()
        }, 200)
    except Exception as e: 
        return make_response({
            "message": f"Error deleting user: {str(e)}"
        }, 400)