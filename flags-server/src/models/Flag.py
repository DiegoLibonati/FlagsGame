from typing import Union
from bson import ObjectId

class Flag:
    def __init__(self, name: str, image: str, _id: ObjectId = None) -> None:
        self.__name = name
        self.__image = image

        self.__id = _id

        self.parse_flag()

    @property
    def id(self) -> ObjectId:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def image(self) -> str:
        return self.__image
    
    @property
    def is_valid(self) -> bool:
        return bool(self.name and self.image)
    
    def set_flag_id(self, id: Union[str, ObjectId]) -> None:
        try:
            self.__id = id if isinstance(id, ObjectId) else ObjectId(id)
        except Exception as e:
            raise ValueError(f"Invalid ID format: {id}.") from e

    def parse_flag(self) -> None:
        self.__name = self.name.strip()
        self.__image = self.image.strip()
    
    def to_dict(self) -> dict[str, str]:
        flag_dict = {
            "name": self.name,
            "image": self.image
        }

        if self.id: flag_dict["_id"] = str(self.id)

        return flag_dict
    
    def __str__(self) -> str:
        return f"\n----- FLAG START -----\n\
        Name: {self.name}\n\
        Image: {self.image}\
        \n----- FLAG END -----\n"