from datetime import datetime
from Helpers.HandleResponseHelper import response
from Models.RoomsModel import RoomsModel
from flask import request
from Core.Flask_Kernel import socketio


class RoomsController:
    def __init__(self):
        self.model = RoomsModel()

    def get_room(self):
        try:
            data = self.model.get_room()
            return response(message=data['message'], isSuccess=data['success'], statusCode=data['code'], data=data['data'])
        except Exception as e:
            return response(message="There is a server error!", data=str(e), isSuccess=False, statusCode=500)

    def add_room(self):
        try:
            json_data = request.get_json()
            room_name = json_data['room_name']
            time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            payload = {
                "name": room_name,
                "inRoom": 0,
                "talks": [],
                "created_at": time,
                "updated_at": time,
            }

            sent = self.model.add_room(payload)
            socketio.emit("stream_rooms", {"status": "create", "data": sent['data']})
            return response(message=sent['message'], isSuccess=sent['success'], statusCode=sent['code'])
        except Exception as e:
            return response(message="There is a server error!", data=str(e), isSuccess=False, statusCode=500)

    def edit_room(self):
        try:
            json_data = request.get_json()

            sent = self.model.edit_room(json_data)
            socketio.emit("stream_rooms", {"status": "update", "data": sent['data']})
            return response(message=sent['message'], isSuccess=sent['success'], statusCode=sent['code'])
        except Exception as e:
            return response(message="There is a server error!", data=str(e), isSuccess=False, statusCode=500)

    def delete_room(self):
        try:
            json_data = request.get_json()

            sent = self.model.delete_room(json_data)
            socketio.emit("stream_rooms", {"status": "delete", "data": sent['data']})
            return response(message=sent['message'], isSuccess=sent['success'], statusCode=sent['code'])
        except Exception as e:
            return response(message="There is a server error!", data=str(e), isSuccess=False, statusCode=500)

    def get_news_chat(self):
        try:
            room_id = request.args.get("room_id")
            result = self.model.get_news_chat(room_id)

            return response(message=result['message'], isSuccess=result['success'], statusCode=result['code'], data=result['data'])
        except Exception as e:
            return response(message="There is a server error!", data=str(e), isSuccess=False, statusCode=500)