from typing import Any

from flask import make_response
from flask import current_app 
from flask import request
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from utils.utils import get_list_users_by_sorted_score
from utils.utils import get_list_modes_names


def top_general() -> dict[str, Any]:
    mode = "general_score"
    users = current_app.mongo.db.users.find()
    data = get_list_users_by_sorted_score(users=users, mode_name_score=mode)

    return make_response({
        "message": "Successfully obtained the global top.",
        "data": data
    }, 200)


def add_or_modify() -> dict[str, Any]:
    method = request.method

    username = request.json['username'].strip()
    password = request.json['password'].strip()
    score_actual = request.json['score']
    mode_name = request.json['mode_name'].strip().lower()

    if not username or not password or not score_actual or not mode_name:
        return make_response({
            "message": "The data entered are not valid.",
            "fields": {
                "username": username,
                "password": password,
                "score": score_actual,
                "mode_name": mode_name
            }
        }, 400)
    
    modes_db = current_app.mongo.db.modes.find()
    modes_names = get_list_modes_names(modes=modes_db)

    if not mode_name in modes_names:
        return make_response({
            "message": "The mode entered does not exist in the database.",
            "fields": {
                "username": username,
                "password": password,
                "score": score_actual,
                "mode_name": mode_name
            }
        }, 400)

    username_db = current_app.mongo.db.users.find_one({"username": username})

    # NOTE: PUT

    if method == "PUT":
        modes_keys = []
        user_db_password = username_db["password"]
        user_db_modes_played = username_db["modes"]

        for mode in user_db_modes_played:
            for key in mode.keys():
                modes_keys.append(key)

        if not username_db:
            return make_response({
                "message": "No valid user was found based on the data entered.",
                "fields": {
                    "username": username,
                    "password": password,
                    "score": score_actual,
                    "mode_name": mode_name
                }
            }, 400)
    
        if username_db and not check_password_hash(user_db_password, password):
            return make_response({
                "message": "Password do not match with that username",
                "fields": {
                    "username": username,
                    "password": password,
                    "score": score_actual,
                    "mode_name": mode_name
                }
            }, 400)
        
        if username_db:
            for index, mode_played in enumerate(user_db_modes_played):
                for mode in mode_played.keys():
                    if mode == mode_name:
                        new_general_score = (username_db["modes"][0]["general_score"] - username_db["modes"][index][mode_name]) + score_actual
                        current_app.mongo.db.users.update_one({"username": username}, {"$set" : {f"modes.{index}.{mode}":score_actual, f"modes.0.general_score":new_general_score}})

            return make_response({
                "message": "User successfully updated"
            }, 201)

    # NOTE: POST

    if method == "POST":

        if not username_db:
            modes = [{"general_score": score_actual}]

            for name in modes_names:
                if name == mode_name:
                    modes.append({str(name).lower(): score_actual})
                else:
                    modes.append({str(name).lower(): 0})

            current_app.mongo.db.users.insert_one({
                'username': username,
                'password': generate_password_hash(password),
                'modes': modes
            })

            return make_response({
                "message":"User successfully added"
            }, 201)
        
        if username_db:
            return make_response({
                "message": "There is a user with that username.",
                "fields": {
                    "username": username,
                    "password": password,
                    "score": score_actual,
                    "mode_name": mode_name
                }
            }, 400)
    
    return make_response({
        "message": "No action was taken.",
        "fields": {
            "username": username,
            "password": password,
            "score": score_actual,
            "mode_name": mode_name
        }
    }, 400)


