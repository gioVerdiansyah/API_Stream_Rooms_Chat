import os
import uuid

from Helpers.HandleResponseHelper import response
from flask import request


def verify_login():
    try:
        json_data = request.get_json()
        username = json_data['username']
        password = json_data['password']
        if username and password:
            if username == os.getenv("APP_LOGIN_USER") and password == os.getenv("APP_LOGIN_PASSWORD"):
                return response(message="Successfully login", data=uuid.uuid4())
            else:
                return response(message="Incorrect Username or Password", isSuccess=False, statusCode=401)
        return response(message="Missing Credentials", statusCode=422, isSuccess=False)
    except Exception as e:
        return response(message="There is a server error!", data=str(e), isSuccess=False, statusCode=500)
