from pydantic import BaseModel, constr


class UserModel(BaseModel):
    username: constr(min_length=1, strip_whitespace=True)
    password: constr(min_length=1, strip_whitespace=True)
    scores: dict[str, int]
    total_score: int
