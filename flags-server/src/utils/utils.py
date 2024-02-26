from flask import make_response

def not_accepted(message: str = "", status: int = 406) -> tuple:

    response = {
        'message': message,
        'status': status
    }

    response.status_code = 406

    return make_response(
        response,
    406)