from bson import ObjectId

class Flag:
    def __init__(self, _id: ObjectId, name: str, image: str) -> None:
        self.__id = _id
        self.__name = name
        self.__image = image

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
        return bool(self.id and self.name and self.image)

    def parse_flag(self) -> None:
        self.__name = self.name.strip()
        self.__image = self.image.strip()
    
    def to_dict(self) -> dict[str, str]:
        return {
            "_id": str(self.id),
            "name": self.name,
            "image": self.image
        }
    
    def __str__(self) -> str:
        return f"\n----- FLAG START -----\n\
        Id: {self.id}\n\
        Name: {self.name}\n\
        Image: {self.image}\
        \n----- FLAG END -----\n"