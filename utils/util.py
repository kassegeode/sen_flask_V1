from _dbus_bindings import String
from flask import json


def json_response(payload, status=200):
    return json.dumps(payload), status, {'Content-Type': 'application/json'}

def json_error(payload, status=400):
    return json.dumps(payload), status, {'Content-Type': 'application/json'}


def token_response(payload, status=200):
    return json.dumps(payload), status, {'Content-Type': 'application/json'}


def json_missions(payload, status=200):
    return json.dumps(payload), status, {'Content-Type': 'application/json'}


def json_misison(qmission):
    mision = {
        'ID': String(qmission.id),
        'Name': qmission.name,
        'Type': qmission.type,
        'Status': qmission.status.name,
        'Date': qmission.start_date,
        'Length': qmission.length,
        'RGB_PICTURE': qmission.cam_count,
        'INFRA_PICTURES': qmission.ir_count,
        'INFRA_VIDEOS': qmission.irrec_count,
        'STATE': None,
    },
    return mision


def json_photo(qphoto):
    photo = {
        'id': String(qphoto.id),
        'missionId': String(qphoto.mission_id),
        'width': String(qphoto.width),
        'height': String(qphoto.height),
        'name': qphoto.name,
        'submission': qphoto.subm,
        'size': String(qphoto.size),
        'category': qphoto.category,
        'sgd_alt': String(qphoto.sgd_alt),
        'obj_distance': String(qphoto.obj_distance),
        'rel_alt': String(qphoto.rel_alt),
        'rel_alt_calc': float(qphoto.rel_alt_calc),
        'gimbal_pitch': String(qphoto.gimbal_pitch),
    }
    return photo

def json_photo_status(qphoto,status):
    photo = {
        'id': String(qphoto.id),
        'missionId': String(qphoto.mission_id),
        'width': String(qphoto.width),
        'height': String(qphoto.height),
        'name': qphoto.name,
        'submission': qphoto.subm,
        'size': String(qphoto.size),
        'category': qphoto.category,
        'sgd_alt': String(qphoto.sgd_alt),
        'obj_distance': String(qphoto.obj_distance),
        'rel_alt': String(qphoto.rel_alt),
        'rel_alt_calc': float(qphoto.rel_alt_calc),
        'gimbal_pitch': String(qphoto.gimbal_pitch),
        'status': status,
    }
    return photo


def json_photo_face(qphoto):
    photo = {
        'id': String(qphoto.id),
        'missionId': String(qphoto.mission_id),
        'width': String(qphoto.width),
        'height': String(qphoto.height),
        'name': qphoto.name,
        'size': String(qphoto.size),
        'category': qphoto.category,
        'sgd_alt': String(qphoto.sgd_alt),
        'obj_distance': String(qphoto.obj_distance),
        'rel_alt': String(qphoto.rel_alt),
        'rel_alt_calc': float(qphoto.rel_alt_calc),
        'gimbal_pitch': String(qphoto.gimbal_pitch),
    }
    return photo


def json_schema_form(jsc):
    schema = {
        'id': String(jsc.id),
        'schema': jsc.schema,
        'uischema': String(jsc.uischema)
    }
    return schema
''' def format_form_degradation(form):
    features = form['features']
    if len(features) > 0:
        coordinates = features['geometry']['coordinates']
        for cor in enumerate(coordinates):
            for c in enumerate(cor):
                float(c) '''