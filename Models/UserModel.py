import datetime
from datetime import datetime, timedelta
from Models.main import ModelMain
from pymongo import DESCENDING


class UserModel(ModelMain):
    def __init__(self):
        super().__init__()
        self.collection = self.mongo_client[self.db_name][self.user_collection]
        self.selected_column = {"_id": 1, "username": 1}

    def get_users(self):
        collection = self.collection
        users_data = list(collection.find({}, self.selected_column).sort("_id", DESCENDING))

        for room in users_data:
            room['_id'] = str(room['_id'])

        return {"success": True, "data": users_data, "code": 200, "message": "Successfully get data!"}

    def user_join(self, data):
        collection = self.collection

        hasExist = collection.find_one({"username": data['username']})
        payload = {
            "username": data['username'],
            "join_at": datetime.now()
        }

        if hasExist:
            latest_chat = hasExist.get("latest_chat")
            if latest_chat:
                current_time = datetime.utcnow()

                if latest_chat > current_time:
                    collection.delete_one(hasExist)
                    collection.insert_one(payload)
                    return {"message": "Successfully join", "code": 200, "success": True}

            return {"message": "User has already taken", "code": 409, "success": False}

        collection.insert_one(payload)
        return {"message": "Successfully join", "code": 200, "success": True}
