from Core.Flask_Kernel import app
from Http.Middleware.VerifyAPIToken import require_api_key
from Http.Controllers.API.LoginController import verify_login
from Http.Controllers.API.RoomsController import RoomsController
from werkzeug.exceptions import HTTPException
from Helpers.HandleResponseHelper import get_struc
from flask import json


def __init_api__():
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        response = e.get_response()
        response.data = json.dumps(get_struc(message=e.name, data=e.description, isSuccess=False, statusCode=e.code))
        response.content_type = "application/json"
        return response

    @app.before_request
    @require_api_key
    def validate_token():
        pass

    @app.route("/api/admin/login", methods=["POST"])
    def login():
        return verify_login()

    @app.route("/api/admin/room/add", methods=["POST"])
    def add_room():
        room = RoomsController()
        return room.add_room()

    @app.route("/api/admin/room/edit", methods=["PUT"])
    def edit_room():
        room = RoomsController()
        return room.edit_room()

    @app.route("/api/admin/room/delete", methods=["DELETE"])
    def delete_room():
        room = RoomsController()
        return room.delete_room()
