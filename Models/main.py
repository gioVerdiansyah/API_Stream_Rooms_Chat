import os

from pymongo import MongoClient

class ModelMain:
    def __init__(self):
        self.mongo_client = MongoClient(os.getenv("APP_DB_URL"))
        self.db_name = os.getenv("APP_DB_NAME")
        self.room_collection = "rooms"

    def __setup__(self):
        db = self.mongo_client[self.db_name]

        if self.room_collection not in db.list_collection_names():
            db.create_collection(self.room_collection)