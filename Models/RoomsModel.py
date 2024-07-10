import json

from Models.main import ModelMain
from Core.Flask_Kernel import socketio
from bson import ObjectId


class RoomsModel(ModelMain):
    def __init__(self):
        super().__init__()
        self.collection = self.mongo_client[self.db_name][self.room_collection]
        self.selected_column = {"_id": 1, "name": 1, "inRoom": 1}

    def add_room(self, data):
        collection = self.collection

        collection.insert_one(data)

        data = collection.find_one({"_id": data["_id"]}, self.selected_column)
        data["_id"] = str(data["_id"])
        socketio.emit("stream_rooms", {"status": "create", "data": data})

        return {"success": True, "message": "Successfully add room", "code": 200}

    def edit_room(self, payload):
        collection = self.collection
        data = payload['data']

        isExist = collection.find_one({"_id": ObjectId(data['id'])}, self.selected_column)
        if not isExist:
            return {"success": False, "message": "Data is not found!", "code": 404}

        collection.update_one(isExist, {"$set": data})

        isExist['_id'] = str(isExist['_id'])
        socketio.emit("stream_rooms", {"status": "update", "data": isExist})

        return {"success": True, "message": "Successfully edit room", "code": 200}

    def delete_room(self, payload):
        collection = self.collection
        room_id = payload['id']

        isExist = collection.find_one({"_id": ObjectId(room_id)}, self.selected_column)
        if not isExist:
            return {"success": False, "message": "Data is not found!", "code": 404}

        collection.delete_one(isExist)

        isExist['_id'] = str(isExist['_id'])
        socketio.emit("stream_rooms", {"status": "delete", "data": isExist})

        return {"success": True, "message": "Successfully delete room", "code": 200}
