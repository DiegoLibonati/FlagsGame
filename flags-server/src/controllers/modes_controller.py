from bson import ObjectId

from flask import make_response
from flask import current_app
from flask import request
from flask import Response

from src.models.Mode import Mode
from src.models.UserManager import UserManager
from src.models.ModeManager import ModeManager


def get_modes() -> Response:
    mode_manager = ModeManager()
    modes = current_app.mode_repository.get_all_modes()

    if modes: mode_manager.add_modes(modes=modes)

    data = mode_manager.parse_items()

    return make_response({
        "message": "Successfully obtained modes.",
        "data": data
    }, 200)


def find_mode(name : str) -> Response:
    if not name:
        return make_response({
            "message": f"A game mode with name {name} was not found, please enter valid fields.",
            "data": None
        }, 400)

    mode = current_app.mode_repository.get_mode_by_name(name=name)

    if not mode:
        return make_response({
            "message": f"A game mode with name {name} was not found, please enter valid fields.",
            "data": None
        }, 404)

    mode = Mode(**mode)
    data = mode.to_dict()

    return make_response({
        "message": "Successfully obtained the requested mode.",
        "data": data
    }, 200)


def add_mode() -> Response:
    name = request.json.get('name', "").strip()
    description = request.json.get('description', "").strip()
    timeleft = request.json.get('timeleft')
    multiplier = request.json.get('multiplier')

    if not name or not description or not timeleft or not multiplier:
        return make_response({
            "message": f"The mode could not be added because the fields entered are not valid.",
            "data": None
        }, 400)

    id_mode = current_app.mode_repository.insert_mode(mode={
        'name': name,
        'description': description,
        'timeleft': timeleft,
        'multiplier': multiplier,
    })

    mode = Mode(
        _id = id_mode,
        name = name,
        description = description,
        multiplier = multiplier,
        timeleft = timeleft
    )
    data = mode.to_dict()

    return make_response({
        "message": f"Successfully created new mode.",
        "data": data
    }, 201)


def top_mode(mode: str) -> Response:
    mode_manager = ModeManager()
    mode_name = mode.lower()

    modes = current_app.mode_repository.get_all_modes()

    if modes: mode_manager.add_modes(modes=modes)

    mode_names = mode_manager.get_modes_names()

    if not modes or not mode_name in mode_names:
        return make_response({ 
            "message": "The top could not be obtained as requested.",
            "data": []
        }, 404)
    
    user_manager = UserManager()
    users = current_app.user_repository.get_all_users() 

    if users: user_manager.add_users(users=users)

    data = user_manager.get_users_top_ten(mode_name=mode_name)

    return make_response({
        "message": "The top ten of the requested mode was obtained.",
        "data": data
    }, 200)


def delete_mode(id: str) -> Response:
    try:
        object_id = ObjectId(id)
        document = current_app.mode_repository.get_mode_by_id(mode_id=object_id)

        if not document: 
            return make_response({
                "message": f"No mode found with id: {id}.",
                "data": None
            }, 404)
        
        mode = Mode(**document)

        current_app.mode_repository.delete_mode_by_id(mode_id=mode.id)

        return make_response({
            "message": f"Mode with id: {id} was deleted.",
            "data": mode.to_dict()
        }, 200)
    except Exception as e: 
        return make_response({
            "message": f"Error deleting mode: {str(e)}"
        }, 400)