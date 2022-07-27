# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from api.utils import responses as resp
from api.utils.responses import response_with


auth_routes = Blueprint("auth_routes", __name__)


@auth_routes.route('/verify', methods=['POST'])
@jwt_required
def verify_token():
    identity = get_jwt_identity()
    return response_with(resp.SUCCESS_200, value={'user': identity, 'message': '有效的金鑰'})
