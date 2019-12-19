from flask import Blueprint, request, jsonify
from utils.cors_decoration import cross_origin
from utils.constants import Constant as constant
from utils.util import json_error

from sdk.auth_sdk import AuthSdk as auth


auth_bp = Blueprint('auth', __name__)


@cross_origin()
@auth_bp.route('/login', methods=['POST'])
def authentication():
    data = request.get_json()
    if request.method == 'POST':
        response_auth = auth.login(data['username'], data['password'])
        if response_auth.get(constant.CODE_STATUS) == constant.VALUE_FAILED:
            return json_error(response_auth)
    else:
        response_auth = {
            constant.CODE_ERR_MSG: constant.BAD_REQUEST,
            constant.CODE_STATUS: constant.VALUE_FAILED
        }
        return json_error(response_auth)

    return jsonify(response_auth)
