from typing import Any

from src.models.Flag import Flag
from src.models.Manager import Manager


class FlagManager(Manager[Flag]):
    def __init__(self) -> None:
        super().__init__(items={}, initializer=Flag)

    @property
    def flags(self) -> list[Flag]:
        return self.items_values
    
    def add_flag(self, flag: Flag) -> None:
        if not flag or not isinstance(flag, Flag): raise TypeError("You must enter a valid flag in order to add it.")

        super()._add_item(item=flag)

    def add_flags(self, flags: list[dict[str, Any]]) -> None:
        if not isinstance(flags, list): raise TypeError("You must enter a valid flags to add its.")

        super()._add_items(items=flags)

    def __str__(self) -> str:
        return f"\n----- FLAGMANAGER START -----\n" \
        f"Flags: {self.parse_items()}\n" \
        f"----- FLAGMANAGER END -----\n"