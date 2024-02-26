from flask import make_response, current_app, request
from bson import json_util
from werkzeug.security import check_password_hash, generate_password_hash
from utils.utils import not_accepted


def top_general() -> tuple:
    top_ten_general = current_app.mongo.db.users.find({},{ "_id":0 ,"username": 1, "modes.general_score":1}).sort([("modes.0.general_score", -1)]).limit(10)
    
    response = json_util.dumps(top_ten_general)

    return make_response(
        response,
    200)


def add_or_modify() -> tuple:
    modes_keys = []

    username = request.json['username'].strip()
    password = request.json['password'].strip()
    score_actual = request.json['score']
    mode_name = request.json['mode_name'].strip().lower()

    username_db = current_app.mongo.db.users.find_one({"username": username})
    modes_db = current_app.mongo.db.modes.find()

    try:
        user_db_password = username_db["password"]
        user_db_modes_played = username_db["modes"]

        for mode in user_db_modes_played:
            for key, value in mode.items():
                modes_keys.append(key)
    except:
        pass

    if not username_db and request.method == "POST":

        modes = [{"general_score": score_actual}]

        for mode in modes_db:
            for key, value in mode.items():
                if key == "name":
                    value = str(value).lower()
                    if value == mode_name:
                        modes.append({str(value).lower(): score_actual})
                    else:
                        modes.append({str(value).lower(): 0})

        if username and password and (not username.isspace() and not password.isspace()):
            current_app.mongo.db.users.insert_one({
                'username': username,
                'password': generate_password_hash(password),
                'modes': modes
            })

            response = json_util.dumps({"message":"User successfully added"},)

            return make_response(
                response, 
            201)

        else:
            
            return not_accepted("Username or password invalid", 406)

    elif username_db and request.method == "POST":

        return not_accepted("There is a user with that username", 406)


    elif username_db and request.method == "PUT" and mode_name in modes_keys:

        if check_password_hash(user_db_password, password):

            for index, mode_played in enumerate(user_db_modes_played):
                for mode, _ in mode_played.items():
                    if mode == mode_name:
                        new_general_score = (username_db["modes"][0]["general_score"] - username_db["modes"][index][mode_name]) + score_actual
                        current_app.mongo.db.users.update_one({"username": username}, {"$set" : {f"modes.{index}.{mode}":score_actual, f"modes.0.general_score":new_general_score}})

                        response = json_util.dumps({"message":"User successfully updated"},)

            return make_response(
                response, 
            201)
        else:
            return not_accepted("Password do not match with that username", 406)

    elif username_db and request.method == "PUT" and not mode_name in modes_keys:
        
        new_general_score = score_actual + username_db["modes"][0]["general_score"]

        if check_password_hash(user_db_password, password):

            current_app.mongo.db.users.update_one({"username": username}, {"$push": {"modes":{mode_name: score_actual}, "$set": {"modes.0.general_score": new_general_score}}})

        response = json_util.dumps({"message":"Successfully added mode"},)

        return make_response(
            response, 
        201)

    elif not username_db and request.method == "PUT":
        return not_accepted("There is not a user with that username created", 406)

