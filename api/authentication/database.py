from authentication.schemas import UserInDB


class Database:
    def __init__(self) -> None:
        self.USERS = {
            "johndoe": {
                "username": "johndoe",
                "full_name": "John Doe",
                "email": "johndoe@example.com",
                "hashed_password": "$2b$12$NGGt2h9N.Fi4Rbe2.oSyae5licR/I1N.ITuj5TcbGO0QNUjdyYZzy",  # password1
                "disabled": False,
            },
            "anubrotoghose": {
                "username": "anubrotoghose",
                "full_name": "Anubroto Ghose",
                "email": "anubrotoghose@hotmail.com",
                "hashed_password": "$2b$12$dV5yWIxkUfSaMmzeRfuyUO/.7a73PSduiXohdYp4.zmn0mpgAKd/O",  # abc123
                "disabled": False,
            },
        }

    def get_user(self, username: str) -> UserInDB | None:
        if username in self.USERS:
            return UserInDB(**self.USERS[username])
