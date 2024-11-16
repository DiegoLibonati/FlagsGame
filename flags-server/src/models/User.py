from functools import reduce
from bson import ObjectId

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from src.models.MongoObject import MongoObject

class User(MongoObject):
    def __init__(self, _id: ObjectId, username: str, password: str, scores: dict[str, int], total_score: int) -> None:
        super().__init__(_id=_id)
        self.__username = username
        self.__password = password
        self.__scores = scores
        self.__total_score = total_score

    @property
    def username(self) -> str:
        return self.__username
    
    @property
    def password(self) -> str:
        return self.__password
    
    @property
    def scores(self) -> dict[str, int]:
        return self.__scores
    
    @property
    def total_score(self) -> int:
        return self.__total_score
    
    @property 
    def password_hashed(self) -> str:
        return generate_password_hash(self.password)
   
    def to_dict(self) -> dict[str, str]:
        return {
            "_id": str(self.id),
            "username": self.username,
            "scores": self.scores,
            "total_score": self.total_score
        }
    
    def valid_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)
    
    def update_scores(self, mode_name: str, score: int) -> None:
            self.__scores[mode_name] = score
            
            if not mode_name in self.scores.keys():
                self.__scores["general"] = self.scores.get("general") + score
            else:
                self.__scores["general"] = reduce(lambda a, b: a+b, self.scores.values()) - self.scores.get("general")
                
            self.__total_score = self.scores["general"]
    
    def __str__(self) -> str:
        return f"\n----- USER START -----\n" \
        f"Id: {self.id}\n" \
        f"Username: {self.username}\n" \
        f"Scores: {self.scores}\n" \
        f"Total Score: {self.total_score}\n" \
        f"----- USER END -----\n"