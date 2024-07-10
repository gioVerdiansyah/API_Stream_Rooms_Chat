from flask import jsonify, make_response


def response(message="Successfully get", data=None, isSuccess=True, statusCode=200):
    if data is None:
        data = {}

    response_payload = {
        "meta": {
            "message": message,
            "isSuccess": isSuccess,
            "statusCode": statusCode
        },
        "data": data
    }

    responses = make_response(jsonify(response_payload), statusCode)

    return responses

def get_struc(message="Successfully get", data=None, isSuccess=True, statusCode=200):
    response_payload = {
        "meta": {
            "message": message,
            "isSuccess": isSuccess,
            "statusCode": statusCode
        },
        "data": data
    }
    return  response_payload