import os
from functools import wraps
from flask import request
from Helpers.HandleResponseHelper import response


def require_api_key(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.method == 'OPTIONS':
            return
        try:
            api_key = request.headers.get('x-api-key')
            if not api_key:
                return response(message='Missing or invalid API key', isSuccess=False, statusCode=403)

            if api_key != os.getenv("APP_TOKEN"):
                return response(message='Invalid API key!', isSuccess=False, statusCode=403)

            return func(*args, **kwargs)
        except Exception as e:
            return response(message=str(e), isSuccess=False, statusCode=500)

    return wrapper
