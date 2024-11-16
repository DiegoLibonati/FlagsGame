from abc import ABC
from typing import TypeVar
from typing import Protocol
from typing import Generic
from typing import Callable


class Serializable(Protocol):
    def to_dict(self) -> dict[str, str]:
        ...

T = TypeVar("T", bound=Serializable)

class Manager(ABC, Generic[T]):
    def __init__(self, initializer: Callable[..., T], items: list[T] = []) -> None:
        self.__initializer = initializer
        self.__items: list[T] = items

    @property
    def items(self) -> list[T]:
        return self.__items
    
    @property
    def initializer(self) -> Callable[..., T]:
        return self.__initializer
    
    def _add_item(self, item: T) -> None:
        self.__items.append(item)

    def _add_items(self, items: dict[str, str]) -> None:
        for item_data in items:
            item = self.initializer(**item_data)
            self.__items.append(item)

    def parse_items(self) -> list[dict[str, str]]:
        return [item.to_dict() for item in self.items]
    
    def __str__(self) -> str:
        return f"\n----- MANAGER START -----\n" \
        f"Items: {self.items}\n" \
        f"----- MANAGER END -----\n"