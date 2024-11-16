from bson import ObjectId

from src.models.MongoObject import MongoObject

class Flag(MongoObject):
    def __init__(self, _id: ObjectId, name: str, image: str) -> None:
        super().__init__(_id=_id)
        self.__name = name
        self.__image = image

    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def image(self) -> str:
        return self.__image
    
    @property
    def is_valid(self) -> bool:
        return bool(self.id and self.name and self.image)
    
    def to_dict(self) -> dict[str, str]:
        return {
            "_id": str(self.id),
            "name": self.name,
            "image": self.image
        }
    
    def __str__(self) -> str:
        return f"\n----- FLAG START -----\n" \
        f"Id: {self.id}\n" \
        f"Name: {self.name}\n" \
        f"Image: {self.image}\n" \
        f"----- FLAG END -----\n"