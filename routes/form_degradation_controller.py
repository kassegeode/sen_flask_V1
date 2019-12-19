from flask import Blueprint, request, jsonify
import simplejson as json
from utils.cors_decoration import cross_origin
from utils.constants import Constant as constant
from utils.util import json_error, json_response

from sdk.form_degradation_sdk import FormDegradation as form_d

form_dg_bp = Blueprint('form_dg', __name__)


@cross_origin()
@form_dg_bp.route('/form/get-form-degradation', methods=['POST'])
def get_form_degradation():
    if request.method == 'POST':
        token = request.headers.get('Authorization', None).__str__().strip('""')
        data_request = request.get_json()
        print('DATA REQUEST :::::::::::', data_request)
        if data_request.get('missionId', '') == '':
            response = {
                constant.CODE_ERR_MSG: constant.BAD_REQUEST + ' mission_id NOT SPECIFIED',
                constant.CODE_STATUS: constant.VALUE_FAILED
            }
            return json_error(response)
        if data_request.get('photoId', '') == '':
            response = {
                constant.CODE_ERR_MSG: constant.BAD_REQUEST + ' photo_id NOT SPECIFIED',
                constant.CODE_STATUS: constant.VALUE_FAILED
            }
            return json_error(response)
        ''' if data_request.get('random_id','') == '':
            response = {
                constant.CODE_ERR_MSG: constant.BAD_REQUEST + ' random_id NOT SPECIFIED',
                constant.CODE_STATUS: constant.VALUE_FAILED
            }
            return json_error(response) '''

        mission_id = data_request['missionId']
        photo_id = data_request['photoId']
        #random_id = data_request['random_id']

        response = form_d.get_report_degradation(token, mission_id, photo_id)
        json_string = json.dumps(response, use_decimal=True)
        #data = json.loads(json_string)
        ''' return jsonify(response) '''
        return json_string
    else:
        response = {
            constant.CODE_ERR_MSG: constant.BAD_REQUEST,
            constant.CODE_STATUS: constant.VALUE_FAILED
        }
        return json_error(response)


@cross_origin()
@form_dg_bp.route('/form/save-form-degradation', methods=['POST'])
def save_form_degradation():
    if request.method == 'POST':
        token = request.headers.get('Authorization', None).__str__().strip('""')
        data_request = request.get_json()
        # data_request = {'missionId': '2176843646832215078', 'photoId': '2176871197445195002', 'geojson': '{"type":"FeatureCollection","features":[{"type":"Feature","geometry":{"type":"Polygon","coordinates":[[[3025.097539432152,929.0472534984897],[3025.097539432152,539.1359948234357],[3535.3517791797535,539.1359948234357],[3535.3517791797535,929.0472534984897],[3025.097539432152,929.0472534984897]]]},"properties":{"annotationType":"rectangle","name":"Rectangle 1","annotationId":1,"fill":true,"fillColor":"#00ff00","fillOpacity":0.25,"stroke":true,"strokeColor":"#000000","strokeOpacity":1,"strokeWidth":3}},{"type":"Feature","geometry":{"type":"Polygon","coordinates":[[[3549.7929369084595,1766.634420126302],[3549.7929369084595,1395.9780384228557],[4016.7237034699438,1395.9780384228557],[4016.7237034699438,1766.634420126302],[3549.7929369084595,1766.634420126302]]]},"properties":{"annotationType":"rectangle","name":"Rectangle 2","annotationId":2,"fill":true,"fillColor":"#00ff00","fillOpacity":0.25,"stroke":true,"strokeColor":"#000000","strokeOpacity":1,"strokeWidth":3}},{"type":"Feature","geometry":{"type":"Polygon","coordinates":[[[2856.6173659305855,3273.3285431545974],[2856.6173659305855,2724.5645494637806],[3833.802372239671,2724.5645494637806],[3833.802372239671,3273.3285431545974],[2856.6173659305855,3273.3285431545974]]]},"properties":{"annotationType":"rectangle","name":"Rectangle 3","annotationId":3,"fill":true,"fillColor":"#00ff00","fillOpacity":0.25,"stroke":true,"strokeColor":"#000000","strokeOpacity":1,"strokeWidth":3}}]}'}
        print('DATA REQUEST :::::::::::', data_request)
        if data_request.get('missionId', '') == '':
            response = {
                constant.CODE_ERR_MSG: constant.BAD_REQUEST + ' mission_id NOT SPECIFIED',
                constant.CODE_STATUS: constant.VALUE_FAILED
            }
            return json_error(response)
        if data_request.get('photoId', '') == '':
            response = {
                constant.CODE_ERR_MSG: constant.BAD_REQUEST + ' photo_id NOT SPECIFIED',
                constant.CODE_STATUS: constant.VALUE_FAILED
            }
            return json_error(response)
        if data_request.get('geojson', '') == '':
            response = {
                constant.CODE_ERR_MSG: constant.BAD_REQUEST + ' object geojson NOT SPECIFIED',
                constant.CODE_STATUS: constant.VALUE_FAILED
            }
        ''' if data_request.get('form_degradation','') == '':
            response = {
                constant.CODE_ERR_MSG: constant.BAD_REQUEST + ' object form_degradation NOT SPECIFIED',
                constant.CODE_STATUS: constant.VALUE_FAILED
            }
            return json_error(response) '''

        mission_id = data_request['missionId']
        photo_id = data_request['photoId']
        form_degradation = data_request['geojson']
        print('GEOJSON    ::::: , ', form_degradation)
        response = form_d.save_or_update(token, mission_id, photo_id, form_degradation)
        return jsonify(response)
    else:
        response = {
            constant.CODE_ERR_MSG: constant.BAD_REQUEST,
            constant.CODE_STATUS: constant.VALUE_FAILED
        }
        return json_error(response)


""" @cross_origin
@form_dg_bp.route('/form/schema/degradation', methods=['POST','GET'])
def display_schema_degradation():
    if request.method == 'POST':
        token = req """
