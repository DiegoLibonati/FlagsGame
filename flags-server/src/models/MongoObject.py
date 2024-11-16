from abc import ABC
from abc import abstractmethod
from bson import ObjectId


class MongoObject(ABC):
    def __init__(self, _id: ObjectId) -> None:
        self.__id = _id

    @property
    def id(self) -> ObjectId:
        return self.__id

    @abstractmethod
    def to_dict(self) -> dict[str, str]:
        pass

    def __str__(self) -> str:
        return f"\n----- MONGOOBJECT START -----\n" \
        f"Id: {self.id}\n" \
        f"----- MONGOOBJECT END -----\n"