from Models.UserModel import UserModel
from Helpers.HandleResponseHelper import response
from flask import request


class UserController:
    def __init__(self):
        self.model = UserModel()

    def get_users(self):
        try:
            data = self.model.get_users()
            return response(message=data['message'], isSuccess=data['success'], statusCode=data['code'],
                            data=data['data'])
        except Exception as e:
            return response(message="There is a server error!", data=str(e), isSuccess=False, statusCode=500)

    def join(self):
        try:
            json_data = request.get_json()
            result = self.model.user_join(json_data)

            return response(message=result['message'], isSuccess=result['success'], statusCode=result['code'], data=result['data'])
        except Exception as e:
            return response(message="There is a server error!", data=str(e), isSuccess=False, statusCode=500)