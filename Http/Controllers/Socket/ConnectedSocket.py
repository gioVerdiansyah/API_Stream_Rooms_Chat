import os

from flask import request
from flask_socketio import join_room
from Core.Flask_Kernel import socketio


def socket_connected():
    user_ip = request.remote_addr

    admin_login = request.headers.get("Access-Permission-Admin-Code")
    if admin_login == os.getenv("APP_FERNET_KEY"):
        join_room(admin_login)
    else:
        socketio.emit("stream_logs", f"[NEW CONNECTION] user IP: {user_ip}", room=admin_login)


def socket_disconnected():
    user_ip = request.remote_addr
    socketio.emit("stream_logs", f"[CLOSE CONNECTION] user IP: {user_ip}", room=os.getenv("APP_FERNET_KEY"))
