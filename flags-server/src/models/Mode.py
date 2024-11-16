from bson import ObjectId

from src.models.MongoObject import MongoObject


class Mode(MongoObject):
    def __init__(self, _id: ObjectId, name: str, description: str, multiplier: int, timeleft: int) -> None:
        super().__init__(_id=_id)
        self.__name = name
        self.__description = description
        self.__multiplier = multiplier
        self.__timeleft = timeleft

    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def description(self) -> str:
        return self.__description
    
    @property
    def multiplier(self) -> int:
        return self.__multiplier
    
    @property
    def timeleft(self) -> int:
        return self.__timeleft
    
    def to_dict(self) -> dict[str, str]:
        return {
            "_id": str(self.id),
            "name": self.name,
            "description": self.description,
            "multiplier": self.multiplier,
            "timeleft": self.timeleft,
        }
    
    def __str__(self) -> str:
        return f"\n----- MODE START -----\n" \
        f"Id: {self.id}\n" \
        f"Name: {self.name}\n" \
        f"Description: {self.description}\n" \
        f"Multiplier: {self.multiplier}\n" \
        f"Timeleft: {self.timeleft}\n" \
        f"----- MODE END -----\n"