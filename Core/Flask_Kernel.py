from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__, )
CORS(app, resources={r'/*': {'origins': '*'}}, support_credentials=True)
socketio = SocketIO(app, cors_allowed_origins="*")