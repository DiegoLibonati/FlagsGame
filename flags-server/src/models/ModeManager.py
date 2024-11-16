from typing import Any

from src.models.Mode import Mode
from src.models.Manager import Manager


class ModeManager(Manager[Mode]):
    def __init__(self) -> None:
        super().__init__(items=[], initializer=Mode)

    @property
    def modes(self) -> list[Mode]:
        return self.items
    
    def add_mode(self, mode: Mode) -> None:
        if not mode or not isinstance(mode, Mode): raise TypeError("You must enter a valid mode in order to add it.")

        super()._add_item(item=mode)

    def add_modes(self, modes: list[dict[str, Any]]) -> None:
        if not modes or not isinstance(modes, list): raise TypeError("You must enter a valid modes to add its.")

        super()._add_items(items=modes)

    def get_modes_names(self) -> list[str]:
        return [mode.name.lower() for mode in self.modes]

    def __str__(self) -> str:
        return f"\n----- MODEMANAGER START -----\n" \
        f"Modes: {self.parse_items()}\n" \
        f"----- MODEMANAGER END -----\n"