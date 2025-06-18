from authentication.schemas import UserInDB
from database.mongo import Mongo


class UsersDB(Mongo):
    def __init__(self, database_name: str, collection_name: str) -> None:
        super().__init__(database_name, collection_name)
        self.create_connection()

    def get_user(self, username: str) -> UserInDB | None:
        user = self.COLLECTION.find_one({"username": username})
        if user is not None :
            return UserInDB(**user)
