from Models.RoomsModel import RoomsModel
from Models.UserModel import UserModel
from flask_socketio import join_room, leave_room
from flask import request
from Helpers.HandleResponseHelper import get_struc
from Core.Flask_Kernel import socketio


class RoomController:
    def __init__(self):
        self.room_model = RoomsModel()
        self.user_model = UserModel()
        self.user_id = request.headers.get("user-token")

    def get_latest_user_room(self):
        latest_room = self.user_model.get_record_latest_room(self.user_id)
        result = self.room_model.find_room(latest_room['data']['room_id'])
        result['data']['id'] = result['data']['_id']
        del result['data']['_id']
        leave_room(result['data']['id'])
        join_room(result['data']['id'])
        print(f"[RE-JOINED ROOM] Username {latest_room['data']['username']} joined room {result['data']['name']}")
        socketio.emit("latest_user_room_response", get_struc(message=result['message'], isSuccess=result['success'], statusCode=result['code'], data=result['data']), room=self.user_id)

    def user_join_room(self, room_id):
        join_room(room_id)

        room = self.room_model.find_room(room_id)
        if not room['success']:
            socketio.emit("latest_user_room_response",
                          get_struc(message="Failed get room, room not found", statusCode=room['code'],
                                    isSuccess=False), room=self.user_id)
            return

        user = self.user_model.record_latest_room(self.user_id, room)
        meta = user['meta']

        print(f"[JOINED ROOM] Username {user['data']['username']} joined room {user['data']['name']}")
        socketio.emit("latest_user_room_response",
                      get_struc(message=meta['message'], isSuccess=meta['isSuccess'], data=user['data'],
                                statusCode=meta['statusCode']), room=self.user_id)

    def user_leave_room(self, room_id):
        username = self.user_model.get_username(self.user_id)['data']
        room_name = self.room_model.find_room(room_id)['data']['name']

        leave_room(room_id)
        print(f"[LEAVED ROOM] Username {username} leaved room {room_name}")
        return "Successfully leave room"

    # Chat
    def user_send_chat(self, data):
        room_id = data['room_id']
        message = data['message']
        username = self.user_model.get_username(self.user_id)['data']

        result = self.room_model.send_chat(room_id, message, self.user_id, username)
        print(f"[NEW CHAT] {self.user_id}: {message}")
        socketio.emit("chat_response", {"status": "create", "data": result}, room=room_id)