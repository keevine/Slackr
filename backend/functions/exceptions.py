from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException
from flask_cors import CORS
from json import dumps
from werkzeug.exceptions import HTTPException


class ValueError(HTTPException):
    code = 400
    message = 'No message specified'


class AccessError(HTTPException):
    code = 400
    message = 'No message specified'


def defaultHandler(err):
    response = err.get_response()
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response