from pydantic import BaseModel, constr


class FlagModel(BaseModel):
    name: constr(min_length=1, strip_whitespace=True)
    image: constr(min_length=1, strip_whitespace=True)
