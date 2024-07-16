from Core.Flask_Kernel import socketio

# Sockets
from Http.Middleware.VerifyTokenKey import valid_token
from Http.Controllers.Socket.ConnectedSocket import socket_connected, socket_disconnected
from Http.Controllers.Socket.UserSocketController import UserSocketController
from Http.Controllers.Socket.RoomController import RoomController


def __init_socket__():
    @socketio.on("connect")
    def run_connect():
        if not valid_token():
            return False
        socket_connected()

    @socketio.on("disconnect")
    def run_disconnect():
        socket_disconnected()

    @socketio.on("want_latest_joined_room")
    def run_want_latest_joined_room():
        room = RoomController()
        room.get_latest_user_room()

    @socketio.on("join_room")
    def run_join_room(room_id):
        room = RoomController()
        room.user_join_room(room_id)

    @socketio.on("leave_room")
    def run_leave_room(room_id):
        room = RoomController()
        return room.user_leave_room(room_id)

    # Chat
    @socketio.on("send_chat")
    def run_send_chat(data):
        room = RoomController()
        room.user_send_chat(data)

    @socketio.on("message")
    def run_message(data):
        print(f"Receive Message: {data}")
        return "What the Fuck Do U want?"

    # Username
    @socketio.on("want_username")
    def run_want_username():
        user = UserSocketController()
        user.get_new_username()

    @socketio.on("rename_username")
    def run_rename_username(name):
        user = UserSocketController()
        user.rename_username(name)
