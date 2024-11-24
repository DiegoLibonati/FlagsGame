from abc import ABC
from typing import Any
from typing import TypeVar
from typing import Protocol
from typing import Generic
from typing import Callable


class Serializable(Protocol):
    id: str

    def to_dict(self) -> dict[str, str]:
        ...

T = TypeVar("T", bound=Serializable)

class Manager(ABC, Generic[T]):
    def __init__(self, initializer: Callable[..., T], items: dict[str, T] = {}) -> None:
        self.__initializer = initializer
        self.__items: dict[str, T] = items

    @property
    def items(self) -> dict[str, T]:
        return self.__items
    
    @property
    def items_values(self) -> list[T]:
        return self.items.values()

    @property
    def initializer(self) -> Callable[..., T]:
        return self.__initializer
    
    def _add_item(self, item: T) -> None:
        self.__items[item.id] = item

    def _add_items(self, items: list[dict[str, Any]]) -> None:
        for item_data in items:
            item: T = self.initializer(**item_data)
            self.__items[item.id] = item

    def parse_items(self) -> list[dict[str, str]]:
        return [item.to_dict() for item in self.items_values]
    
    def __str__(self) -> str:
        return f"\n----- MANAGER START -----\n" \
        f"Items: {self.parse_items()}\n" \
        f"----- MANAGER END -----\n"