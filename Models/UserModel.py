import datetime
from datetime import datetime, timedelta
from Models.main import ModelMain
from pymongo import DESCENDING
from bson import ObjectId
from Helpers.HandleResponseHelper import get_struc
from Helpers.HandleHashPassword import encrypt_password, decrypt_password


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
        print(data)

        hasExist = collection.find_one({"username": data['username']})

        if hasExist:
            if data['password'] == decrypt_password(hasExist['password']):
                return {"message": "Successfully join", "code": 200, "success": True, "data": str(hasExist['_id'])}
            return {"message": "Incorrect Password!", "code": 401, "success": False, "data": None}

        payload = {
            "username": data['username'],
            "join_at": datetime.now(),
            "password": encrypt_password(data['password'])
        }

        user_id = collection.insert_one(payload).inserted_id
        return {"message": "Successfully join", "code": 200, "success": True, "data": str(user_id)}

    def get_username(self, user_id):
        collection = self.collection

        get_id = collection.find_one({"_id": ObjectId(user_id)}, {"username"})
        if not get_id:
            return get_struc(message="User ID is not found!", isSuccess=False, statusCode=404)

        return get_struc(data=get_id['username'])

    def rename_username(self, user_id, name):
        collection = self.collection

        user = collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return get_struc(message="User ID is not found!", isSuccess=False, statusCode=404)

        hasExistUsername = collection.find_one({"username": name})
        if hasExistUsername:
            return get_struc(message="User is already taken!", isSuccess=False, statusCode=401)

        collection.update_one(user, {"$set": {"username": name}})
        new_name = collection.find_one({"_id": ObjectId(user_id)}).get('username')

        return get_struc(data=new_name)

    def record_latest_room(self, user_id, room):
        room = room['data']
        room['_id'] = str(room['_id'])
        collection = self.collection

        get_id = collection.find_one({"_id": ObjectId(user_id)}, {"username"})
        if not get_id:
            return get_struc(message="User ID is not found!", isSuccess=False, statusCode=401)

        collection.update_one(get_id, {"$set": {"latest_room": room['_id']}})

        return get_struc(message="Successfully record latest room", data={"id": room['_id'], "name": room['name'], "username": get_id['username']})

    def get_record_latest_room(self, user_id):
        collections = self.collection

        get_user = collections.find_one({"_id": ObjectId(user_id)})
        if not get_user:
            return get_struc(message="User ID is not found!", isSuccess=False, statusCode=401)

        if not get_user.get("latest_room"):
            return get_struc(message="Room is not initializing!", isSuccess=False, statusCode=404)

        return get_struc(data={"room_id": get_user["latest_room"], "username": get_user['username']})