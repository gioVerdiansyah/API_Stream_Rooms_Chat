from datetime import datetime

from Models.main import ModelMain
from bson import ObjectId
from pymongo import DESCENDING


class RoomsModel(ModelMain):
    def __init__(self):
        super().__init__()
        self.collection = self.mongo_client[self.db_name][self.room_collection]
        self.selected_column = {"_id": 1, "name": 1, "inRoom": 1}

    def get_room(self):
        collection = self.collection
        rooms_data = list(collection.find({}, self.selected_column).sort("_id", DESCENDING))

        for room in rooms_data:
            room['_id'] = str(room['_id'])

        return {"success": True, "data": rooms_data, "code": 200, "message": "Successfully get data!"}

    def add_room(self, data):
        collection = self.collection

        collection.insert_one(data)

        data = collection.find_one({"_id": data["_id"]}, self.selected_column)
        data["_id"] = str(data["_id"])

        return {"success": True, "message": "Successfully add room", "code": 200, "data": data}

    def edit_room(self, payload):
        collection = self.collection
        data = payload['data']
        room_id = ObjectId(data['id'])

        isExist = collection.find_one({"_id": room_id}, self.selected_column)
        if not isExist:
            return {"success": False, "message": "Data is not found!", "code": 404}

        data.pop('id', None)
        data['updated_at'] = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        collection.update_one({"_id": room_id}, {"$set": data})

        updated_room = collection.find_one({"_id": room_id}, self.selected_column)
        updated_room['_id'] = str(updated_room['_id'])

        return {"success": True, "message": "Successfully edit room", "code": 200, "data": updated_room}

    def delete_room(self, payload):
        collection = self.collection
        room_id = payload['id']

        isExist = collection.find_one({"_id": ObjectId(room_id)}, self.selected_column)
        if not isExist:
            return {"success": False, "message": "Data is not found!", "code": 404}

        collection.delete_one(isExist)

        isExist['_id'] = str(isExist['_id'])

        return {"success": True, "message": "Successfully delete room", "code": 200, "data": isExist}

    def find_room(self, room_id):
        collection = self.collection

        get_room = collection.find_one({"_id": ObjectId(room_id)}, {"_id", "name"})
        if not get_room:
            return {"success": False, "message": "Data is not found!", "code": 404, "data": None}

        get_room['_id'] = str(get_room['_id'])

        return {"success": True, "message": "Successfully get room", "code": 200, "data": get_room}

    # Socket
    # Chat

    def get_news_chat(self, room_id):
        collection = self.collection

        talks = collection.find_one({"_id": ObjectId(room_id)}).get("talks")

        if not talks:
            return {"success": False, "message": "Data is not found!", "code": 404, "data": None}

        return {"success": True, "message": "Successfully get room", "code": 200, "data": talks}

    def send_chat(self, room_id, message, user_token, username):
        collection = self.collection

        payload = {
            "user_id": user_token,
            "name": username,
            "message": message,
            "chat_at": datetime.now()
        }

        collection.update_one(
            {"_id": ObjectId(room_id)},
            {"$push": {"talks": payload}}
        )

        payload['chat_at'] = str(payload['chat_at'])
        return payload