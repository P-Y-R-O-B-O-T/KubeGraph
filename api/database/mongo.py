import pymongo
import os


class Mongo:
    def __init__(self, database: str, collection: str) -> None:
        self.DATABASE_NAME = database
        self.COLLECTION_NAME = collection

    def create_connection(self) -> None:
        self.DATABASE_CONNECTION = pymongo.MongoClient(
            f"mongodb://{os.getenv("MONGO_INITDB_ROOT_USERNAME")}:{os.getenv("MONGO_INITDB_ROOT_PASSWORD")}@mongo:27017"
        )
        self.DATABASE = self.DATABASE_CONNECTION[self.DATABASE_NAME]
        self.COLLECTION = self.DATABASE[self.COLLECTION_NAME]
