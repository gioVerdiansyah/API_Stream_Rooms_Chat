from Models.UserModel import UserModel
from Core.Flask_Kernel import socketio
from flask import request
from flask_socketio import join_room


class UserSocketController:
    def __init__(self):
        self.model = UserModel()

    def get_new_username(self):
        user_id = request.headers.get("user-token")
        result = self.model.get_username(user_id)
        join_room(user_id)
        socketio.emit("want_username_response", result, room=user_id)