from pydantic import BaseModel, constr


class ModeModel(BaseModel):
    name: constr(min_length=1, strip_whitespace=True)
    description: constr(min_length=1, strip_whitespace=True)
    multiplier: int
    timeleft: int
