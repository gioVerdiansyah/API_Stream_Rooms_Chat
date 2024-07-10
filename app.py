import os
from dotenv import load_dotenv

from Core.Flask_Kernel import app, socketio
from routes import socket, api
from Models.main import ModelMain

load_dotenv()

socket.__init_socket__()
api.__init_api__()
model = ModelMain()
model.__setup__()

if __name__ == "__main__":
    socketio.run(app, debug=True, host=os.getenv("APP_HOST"), port=os.getenv("APP_PORT"), allow_unsafe_werkzeug=True)
