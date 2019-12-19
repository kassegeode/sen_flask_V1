from flask import Blueprint, request, jsonify
from sdk.missions_sdk import Missions as mission
from utils.util import json_missions, json_error
from utils.cors_decoration import cross_origin
from utils.constants import Constant as constant

home_bp = Blueprint('home', __name__)


@cross_origin()
@home_bp.route('/missions', methods=["GET"])
def show():
    if request.method == 'GET':
        token = request.headers.get('Authorization', None).__str__().strip('""')
        response_missions = mission.display_missions(token)
        ''' if response_missions.get(constant.CODE_STATUS) == constant.VALUE_FAILED:
            return json_error(response_missions) '''
    else:
        response = {
            constant.CODE_ERR_MSG: constant.BAD_REQUEST,
            constant.CODE_STATUS: constant.VALUE_FAILED
        }
        return json_error(response)

    return json_missions(response_missions)


@home_bp.route('/report/face/<string:mission_id>', methods=["GET"])
def display_mission(mission_id):
    if request.method == 'GET':
        token = request.headers.get('Authorization', None).__str__().strip('""')
        #response_report_id = mission.get_state_submission(mission_id, token)
        response_report_id = mission.get_state_submission_status(mission_id, token)

        ''' if response_report_id.get(constant.CODE_STATUS) == constant.VALUE_FAILED:
            return json_error(response_report_id) '''

    else:
        response = {
            constant.CODE_ERR_MSG: constant.BAD_REQUEST,
            constant.CODE_STATUS: constant.VALUE_FAILED
        }
        return json_error(response)

    return jsonify(response_report_id)


@home_bp.route('/missions/state/<string:mission_id>', methods=["GET"])
def show_state(mission_id):
    if request.method == 'GET':
        token = request.headers.get('Authorization', None).__str__().strip('""')
        print('MISSION_ID', mission_id)
        response_missions = mission.get_statistics_mission(mission_id, token)
        ''' if response_missions.get(constant.CODE_STATUS) == constant.VALUE_FAILED:
            return json_error(response_missions) '''

    else:
        response = {
            constant.CODE_ERR_MSG: constant.BAD_REQUEST,
            constant.CODE_STATUS: constant.VALUE_FAILED
        }
        return json_error(response)

    return jsonify(response_missions)
