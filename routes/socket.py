from Core.Flask_Kernel import socketio
from flask import request

# Sockets
from Http.Middleware.VerifyTokenKey import valid_token
from Http.Controllers.Socket.ConnectedSocket import socket_connected


def __init_socket__():
    @socketio.on("connect")
    def run_connect():
        if not valid_token():
            return False
        socket_connected()

    # @socketio.on("join_room")
    # def run_join_room():
    #

    @socketio.on("message")
    def run_message(data):
        print(f"Receive Message: {data}")
        return "What the Fuck Do U want?"

    # Admin Streaming Data Event
    # stream_rooms