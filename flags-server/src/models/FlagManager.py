from src.models.Flag import Flag

class FlagManager:
    def __init__(self) -> None:
        self.__flags: list[Flag] = []

    @property
    def flags(self) -> list[Flag]:
        return self.__flags
    
    def add_flag(self, flag: Flag) -> None:
        if not flag or not isinstance(flag, Flag): raise TypeError("You must enter a valid flag in order to add it.")

        self.__flags.append(flag)

    def parse_flags(self) -> list[dict[str, str]]:
        return [flag.to_dict() for flag in self.flags]

    def __str__(self) -> str:
        return f"\n----- FLAG START -----\n\
        Flags: {self.flags}\
        \n----- FLAG END -----\n"