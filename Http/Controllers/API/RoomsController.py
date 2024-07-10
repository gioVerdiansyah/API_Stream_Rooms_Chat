from datetime import datetime
from Helpers.HandleResponseHelper import response
from Models.RoomsModel import RoomsModel
from flask import request


class RoomsController:
    def __init__(self):
        self.model = RoomsModel()

    def add_room(self):
        try:
            json_data = request.get_json()
            room_name = json_data['room_name']
            time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            payload = {
                "name": room_name,
                "inRoom": 0,
                "created_at": time,
                "updated_at": time,
            }

            sent = self.model.add_room(payload)
            return response(message=sent['message'], isSuccess=sent['success'], statusCode=sent['code'])
        except Exception as e:
            return response(message="There is a server error!", data=str(e), isSuccess=False, statusCode=500)

    def edit_room(self):
        try:
            json_data = request.get_json()

            sent = self.model.edit_room(json_data)
            return response(message=sent['message'], isSuccess=sent['success'], statusCode=sent['code'])
        except Exception as e:
            return response(message="There is a server error!", data=str(e), isSuccess=False, statusCode=500)

    def delete_room(self):
        try:
            json_data = request.get_json()

            sent = self.model.delete_room(json_data)
            return response(message=sent['message'], isSuccess=sent['success'], statusCode=sent['code'])
        except Exception as e:
            return response(message="There is a server error!", data=str(e), isSuccess=False, statusCode=500)
