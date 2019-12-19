from flask import Blueprint, request, jsonify, current_app
from schemas.form_schema import input_form_schema, json_schemas
from sdk.form_sdk import FormSDK as form, get_cached_image_moz_v1, get_cached_image_v1
import httplib2
from utils.constants import Constant as constant
from utils.util import json_error

form_bp = Blueprint('form', __name__)


@form_bp.route('/form/save-report-data', methods=["POST"])
def save_mission_report_data():

    if request.method == 'POST':
        token = request.headers.get('Authorization', None).__str__().strip('""')
        data_save = request.get_json()
        response = form.save_report_data(token, data_save)
        print('DATA = ', data_save)
        ''' if response.get(constant.CODE_STATUS) == constant.VALUE_FAILED:
            return json_error(response) '''
    else:
        response = {
            constant.CODE_ERR_MSG: constant.BAD_REQUEST,
            constant.CODE_STATUS: constant.VALUE_FAILED
        }
        return json_error(response)

    return jsonify(response)


@form_bp.route('/form/clean-report-data', methods=["POST"])
def clean_mission_report_data():

    if request.method == 'POST':
        token = request.headers.get('Authorization', None).__str__().strip('""')
        data_save = request.get_json()
        response = form.clean_report_data(token, data_save)
        ''' if response.get(constant.CODE_STATUS) == constant.VALUE_FAILED:
            return json_error(response) '''
    else:
        response = {
            constant.CODE_ERR_MSG: constant.BAD_REQUEST,
            constant.CODE_STATUS: constant.VALUE_FAILED
        }
        return json_error(response)

    return jsonify(response)


@form_bp.route('/form/get-report-data', methods=["POST"])
def get_mission_report_data():
    if request.method == 'POST':
        token = request.headers.get('Authorization', None).__str__().strip('""')
        data_request = request.get_json()
        mission_id = data_request['missionID']
        id_photos = data_request['id']
        print('MISSION_ID', mission_id)
        print('PHOTO_ID', id_photos)
        print('DATA ==', data_request)
        response = form.get_report_data(token, mission_id, id_photos)
        ''' if response.get(constant.CODE_STATUS) == constant.VALUE_FAILED:
            return json_error(response) '''
    else:
        response = {
            constant.CODE_ERR_MSG: constant.BAD_REQUEST,
            constant.CODE_STATUS: constant.VALUE_FAILED
        }
        return json_error(response)

    return jsonify(response)


@form_bp.route('/form/schema/<string:mission_type>', methods=['GET'])
def display_schema(mission_type):
    if request.method == 'GET':
        token = request.headers.get('Authorization', None).__str__().strip('""')
        mission_type = 1
        if len(form.display_schema_form(token, mission_type, "")) == 0:
            #response = input_form_schema
            response = json_schemas
        else:
            response = form.display_schema_form(token, mission_type, "")
            ''' if response.get(constant.CODE_STATUS) == constant.VALUE_FAILED:
                return json_error(response) '''
    else:
        response = {
            constant.CODE_ERR_MSG: constant.BAD_REQUEST,
            constant.CODE_STATUS: constant.VALUE_FAILED
        }
        return json_error(response)

    return jsonify(response)


@form_bp.route('/report/photoID', methods=["POST"])
def get_image():
    if request.method == 'POST':
        data = request.get_json()
        photo_id = int(data["id"])
        mission_id = int(data["missionID"])
        token = request.headers.get('Authorization', None).__str__().strip('""')
        request_photo_id = get_cached_image_v1(photo_id, mission_id, token)
        url_report_split = current_app.config["URL_SERVER_TO_SPLIT"]
        url_server_images = current_app.config["URL_SERVER_IMAGES"]
        response_url_files = httpGet(url_report_split, params="url="+url_server_images +
                                     request_photo_id["path"]).__str__().strip("b'")
    else:
        response = {
            constant.CODE_ERR_MSG: constant.BAD_REQUEST,
            constant.CODE_STATUS: constant.VALUE_FAILED
        }
        return json_error(response)

    return response_url_files


@form_bp.route('/report/mosaique/<string:mission_id>', methods=["GET"])
def get_url_moz(mission_id):
    token = request.headers.get('Authorization', None).__str__().strip('""')
    if request.method == 'GET':
        response = get_cached_image_moz_v1(mission_id, token)
        #response = get_cached_image_moz(mission_id, token)
        ''' if response.get(constant.CODE_STATUS) == constant.VALUE_FAILED:
            return json_error(response) '''
    else:
        response = {
            constant.CODE_ERR_MSG: constant.BAD_REQUEST,
            constant.CODE_STATUS: constant.VALUE_FAILED
        }
        return json_error(response)
    return jsonify(response)


def httpGet(url, params=""):
    try:
        conn = httplib2.Http()
        response, content = conn.request(url + '?' + params, "GET")
        print(response)
        return content

    except httplib2.HttpLib2ErrorWithResponse:
        print("Exception Levée Par Le serveur Spring Pour Le Split De L'IMAGE")
        return False
