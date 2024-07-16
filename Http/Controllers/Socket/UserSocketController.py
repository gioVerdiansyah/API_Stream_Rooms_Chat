from Models.UserModel import UserModel
from Core.Flask_Kernel import socketio
from flask import request
from flask_socketio import join_room


class UserSocketController:
    def __init__(self):
        self.model = UserModel()
        self.user_id = request.headers.get("user-token")

    def get_new_username(self):
        user_id = self.user_id
        result = self.model.get_username(user_id)
        join_room(user_id)
        socketio.emit("want_username_response", result, room=user_id)

    def rename_username(self, name):
        result = self.model.rename_username(self.user_id, name)
        socketio.emit("want_username_response", result, room=self.user_id)