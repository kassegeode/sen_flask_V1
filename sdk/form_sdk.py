from flagshipcore.flagship.libserver import QualiticsFlagship, QualiticsFlagshipException, MissionOpenMode, MissionStatus
from flask import current_app, url_for
from .services import Service as srv, search_data_form, get_json_langue
import os
from utils.constants import Constant as constant

from _dbus_bindings import String



def connect_sdk_flagship():
    return QualiticsFlagship(current_app.config['FLAGSHIP_SERVER'])


class FormSDK(object):

    @staticmethod
    def display_schema_form(token, mission_type, schema_key):
        rest = connect_sdk_flagship()

        if token is not None and rest.authenticated(token):
            try:
                json_schema_form = rest.adm_get_jsonform_data(mission_type, schema_key)
                json_schema = []
                for jsc in json_schema_form:
                    json_schema.append(srv.form_schema(jsc))
                return json_schema

            except QualiticsFlagshipException as ex:
                mess = "/ {}".format(ex).upper()
                response = {
                    constant.CODE_ERR_MSG: constant.VALUE_ERROR_GET_SCHEMAS + mess,
                    constant.CODE_STATUS: constant.VALUE_FAILED
                }
                return response

    @staticmethod
    def save_report_data(token, data, mission_id="DEFAULT"):
        rest = connect_sdk_flagship()
        if data.get('missionId', '') == '':
            mission_id = mission_id
        else:
            mission_id = data['missionId']

        if token is not None and rest.authenticated(token):
            try:
                mission = srv.get_mission(rest, mission_id)

                if mission.status == MissionStatus.UPLOADED:
                    rest.adm_open_mission(mission, MissionOpenMode.MODE_JSON)

                report_data = srv.get_report_data(rest, mission)

                rest.adm_set_report_data(mission, srv.update_report_data(report_data, srv.format_data_report(data)))

                response = {
                    constant.CODE_STATUS: constant.VALUE_SUCCESS,
                    constant.CODE_SUC_MSG: constant.TEXT_FORM_SAVE_SUCCESS,
                }

            except QualiticsFlagshipException as ex:
                mess = "/ {}".format(ex).upper()
                response = {
                    constant.CODE_STATUS: constant.VALUE_FAILED,
                    constant.CODE_ERR_MSG: constant.TEXT_ERR_SAVE_SCHEMA + mess
                }
            return response

    @staticmethod
    def clean_report_data(token, data):
        rest = connect_sdk_flagship()
        mission_id = data['missionId']

        if token is not None and rest.authenticated(token):
            try:
                mission = srv.get_mission(rest, mission_id)

                report_data = srv.get_report_data(rest, mission)

                rest.adm_set_report_data(mission, srv.clean_report_data(report_data, srv.format_data_report(data)))

                response = {
                    constant.CODE_STATUS: constant.VALUE_SUCCESS,
                    constant.CODE_SUC_MSG: constant.TEXT_FORM_SAVE_SUCCESS,
                }

            except QualiticsFlagshipException as ex:
                mess = "/ {}".format(ex).upper()
                response = {
                    constant.CODE_STATUS: constant.VALUE_FAILED,
                    constant.CODE_ERR_MSG: constant.TEXT_ERR_SAVE_SCHEMA + mess
                }
            return response

    @staticmethod
    def get_report_data(token, mission_id, id_photos):
        rest = connect_sdk_flagship()
        if token is not None and rest.authenticated(token):
            try:
                mission = srv.get_mission(rest, mission_id)
                if srv.verif_id_photo(rest, mission, id_photos):
                    report_data = srv.get_report_data(rest, mission)
                    if report_data is not None:
                        response = search_data_form(report_data, id_photos)
                        if response is None:
                            response = {
                                'id': id_photos,
                                constant.CODE_STATUS: "",
                                constant.CODE_DESCRIPTION: ""
                            }
                            return get_json_langue(srv.format_data_report(response))
                        else:
                            return get_json_langue(srv.format_data_report(response))

                    if report_data is None:
                        response = {
                            'id': id_photos,
                            constant.CODE_STATUS: "",
                            constant.CODE_DESCRIPTION: ""
                        }
                        return get_json_langue(srv.format_data_report(response))

            except QualiticsFlagshipException as ex:
                mess = "/ {}".format(ex).upper()
                response = {
                    constant.CODE_STATUS: constant.VALUE_FAILED,
                    constant.CODE_ERR_MSG: constant.TEXT_ERR_GET_DATA_FORM + mess
                }

            return response


def get_cached_image_v1(photo_id, mission_id, token, status="DEFAULT", face="DEFAULT", altitude="DEFAULT"):
    rest = connect_sdk_flagship()

    if status == "DEFAULT":
        tmp_folder = current_app.config["FOLDER_TMP"]
        img_scale = float(current_app.config["IMG_SCALE"])
    else:
        tmp_folder = current_app.config["FOLDER_TMP_MOS"]
        img_scale = float(current_app.config["IMG_SCALE_PHOTO_MOS"])

        if status == 'Good' or status == "BON":
            statuss = 'BON'
        elif status == 'Low Degradation' or status == "FAIBLE DEGRADATION":
            statuss = 'FAIBLE DEGRADATION'
        elif status == 'Strong degradation' or status == "FORTE DEGRADATION":
            statuss = 'FORTE DEGRADATION'
        elif status == 'Critical' or status == "CRITIQUE":
            statuss = 'CRITIQUE'
        elif status == 'NOT TREATED' or status == "NON TRAITÉE" or status == "" or status == "NON TRAITEE":
            statuss = 'NON TRAITEE'
        else:
            statuss = "NON TRAITEE"

        if face.split(' ')[0] == constant.kEY_FACE_M:
            type_subm = constant.kEY_FACE_MOZ
            f = face
        elif face.split(' ')[0] == constant.kEY_ARRET:
            type_subm = constant.kEY_ARRET_MOZ
            f = 'Arete {}'.format(face.split(' ')[1])
        else:
            type_subm = None
            f = None

    tmp_path = os.path.join(current_app.config["STATIC_FOLDER"], tmp_folder)

    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)

    img_name = "{}.jpeg".format(photo_id)
    img_path = os.path.join(tmp_path, img_name)

    filename = os.path.join(tmp_folder, img_name)

    if not os.path.isfile(img_path):
        if token is not None and rest.authenticated(token):
            mission = srv.get_mission(rest, mission_id)

            photos_info = srv.get_photo_info(rest, mission, photo_id)

            try:
                raw_image = rest.com_get_photo(photos_info, img_scale)

                with open(img_path, "wb") as fh:
                    fh.write(raw_image)

            except QualiticsFlagshipException as ex:
                mess = "/ {}".format(ex).upper()
                print(mess)
                filename = os.path.join(current_app.config['FOLDER_ASSETS'], 'not-available.png')

    if status == "DEFAULT":
        photo_data = {"id": String(photo_id), "path": url_for('static', filename=filename)}
    else:
        url = current_app.config["URL_SERVER_IMAGES"]
        photo_data = {
            constant.CODE_ID: String(photo_id),
            'face': f,
            'type': type_subm,
            'path': url + url_for('static', filename=filename),
            "id_mission": String(mission_id),
            'altitude': float(altitude),
            constant.CODE_STATUS: statuss
        }

    return photo_data


def get_cached_image_moz_v1(mission_id, token):
    rest = connect_sdk_flagship()
    if token is not None and rest.authenticated(token):
        try:
            mission = srv.get_mission(rest, mission_id)
            photos_info = rest.com_get_mission_photos(mission)
            json_url_list = []
            json_form = srv.get_report_data(rest, mission)
            list_face = list_submission(photos_info)

            for photo in photos_info:
                status = srv.get_status_json_data_form(json_form, photo.id)

                if status is not None:
                    state = status
                else:
                    state = ""

                f = photo.subm
                for F in list_face:
                    if f == F:
                        json_url_list.append(get_cached_image_v1(photo.id, mission_id, token,
                                                                 status=state, face=f, altitude=photo.rel_alt_calc))

            return json_url_list

        except QualiticsFlagshipException as ex:
            mess = "/ {}".format(ex).upper()
            error = {
                constant.CODE_STATUS: constant.VALUE_FAILED,
                constant.CODE_ERR_MSG: constant.TEXT_ERROR_GET_IMAGE_MOZ + mess,
                'path': None
            }
            return error


def list_submission(qphotos):
    init_List = []
    ls_ordered = []
    for ph in qphotos:
        submission = ph.subm
        if len(init_List) == 0:
            init_List.append(submission)
        elif len(init_List) > 0:
            if ph.subm not in init_List:
                init_List.append(ph.subm)
                
    if len(init_List) == 1:
        return init_List

    for i in range(len(init_List)):
        face = [elem for elem in init_List if 'Face {}'.format(i+1) in elem]
        arret = [elem for elem in init_List if 'Arête {}'.format(i+1) in elem]
        ls_ordered.extend(face)
        ls_ordered.extend(arret)

    print('ORDERED LIST FACE ::::: ', ls_ordered)

    return ls_ordered
