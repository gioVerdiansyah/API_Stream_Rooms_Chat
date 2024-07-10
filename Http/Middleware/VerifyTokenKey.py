import os
from flask import request


def valid_token():
    token = request.headers.get('x-socket-key')
    if not token or not validate_token(token):
        print(f"[NEW CONNECTION REJECTED] {request.remote_addr}")
        return False
    return True


def validate_token(token):
    return token == os.getenv("APP_TOKEN")
