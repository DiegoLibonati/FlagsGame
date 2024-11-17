from typing import Any

from src.models.User import User
from src.models.Manager import Manager


class UserManager(Manager[User]):
    def __init__(self) -> None:
        super().__init__(items=[], initializer=User)

    @property
    def users(self) -> list[User]:
        return self.items
    
    def add_user(self, user: User) -> None:
        if not user or not isinstance(user, User): raise TypeError("You must enter a valid user in order to add it.")

        super()._add_item(item=user)

    def add_users(self, users: list[dict[str, Any]]) -> None:
        if not users or not isinstance(users, list): raise TypeError("You must enter a valid users to add its.")

        super()._add_items(items=users)

    def get_users_top_ten(self, mode_name: str) -> dict[str, Any]: 
        data = []
    
        for user in self.users:
            user_in_top = {}

            user_in_top["_id"] = str(user.id)
            user_in_top["username"] = user.username

            if mode_name == "general": user_in_top["score"] = user.total_score                        
            else: user_in_top["score"] = user.scores.get(mode_name, 0)                        

            data.append(user_in_top)

        if not data:
            return []

        data.sort(key=lambda x: x['score'], reverse=True)

        return data[:10]

    def __str__(self) -> str:
        return f"\n----- USERMANAGER START -----\n" \
        f"Users: {self.parse_items()}\n" \
        f"----- USERMANAGER END -----\n"