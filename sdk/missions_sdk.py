from flagshipcore.flagship.libserver import QualiticsFlagship, QualiticsFlagshipException
from flask import current_app
from utils.util import json_misison, json_photo_face, json_photo,json_photo_status
from utils.constants import Constant as constant
from .services import Service as srv
from .form_sdk import get_cached_image_moz_v1
from operator import attrgetter


def connect_sdk_flagship():
    return QualiticsFlagship(current_app.config['FLAGSHIP_SERVER'])


class Missions(object):

    @staticmethod
    def display_missions(token):
        rest = connect_sdk_flagship()
        missions = []
        cmpt = 0
        try:
            if token is not None and rest.authenticated(token):
                missions_List = rest.adm_get_missions()
                for m in missions_List:
                    cmpt += 1
                    missions.extend(json_misison(m))
                    print("Chargement Des Missions : ", cmpt)
                data = missions
        except QualiticsFlagshipException as ex:
            mess = "/ {}".format(ex).upper()
            data = {
                constant.CODE_ERR_MSG: constant.VALUE_ERR_SHOW_MISSIONS + mess,
                constant.CODE_STATUS: constant.VALUE_FAILED
            }
        return data

    @staticmethod
    def get_statistics_mission(mission_id, token):
        rest = connect_sdk_flagship()
        if token is not None and rest.authenticated(token):
            try:
                photos_info = get_cached_image_moz_v1(mission_id, token)
                responses = []
                
                mission = srv.get_mission(rest,mission_id)
                qphotos = rest.com_get_mission_photos(mission) 
                list_submission = get_list_submission(qphotos)
                
                for i,submission in enumerate(list_submission):
                    name = "{}".format(submission)
                    if name.split(' ')[0] == 'Arête':
                        s = 'Arete {}'.format(name.split(' ')[1])
                        #subm_list = [x for x in photos_info if x['face'] == list_submission[i]]
                        subm_list = [x for x in photos_info if x['face'] == s]
                    else:
                        subm_list = [x for x in photos_info if x['face'] == list_submission[i]]
                    print(subm_list)
                    status_list = get_list_status(subm_list)
                    format_status = format_respose_statut(name, status_list)
                    responses.append(format_status)

            except QualiticsFlagshipException as ex:
                mess = "/ {}".format(ex).upper()
                responses = {
                    constant.CODE_ERR_MSG: mess,
                    constant.CODE_STATUS: constant.VALUE_FAILED
                }

            return responses

    @staticmethod
    def get_state_submission(mission_id, token):
        rest = connect_sdk_flagship()
        if token is not None and rest.authenticated(token):
            try:
                mission = srv.get_mission(rest, mission_id)
                responses = []
                l_faces = []
                qphotos = rest.com_get_mission_photos(mission)
                list_submission = get_list_submission(qphotos)         
                    
                
                for ph in qphotos:
                    l_faces.append(json_photo(ph))

                for i, submission in enumerate(list_submission):
                    name = "{}".format(submission)
                    type_submission = "{}".format(name.split(' ')[0]).lower()
                    missions = [x for x in l_faces if x['submission'] == list_submission[i]]
                    format_response = format_response_subm(name, missions, type_submission)
                    responses.append(format_response)

                return responses

            except QualiticsFlagshipException as ex:
                mess = "/ {}".format(ex).upper()
                response = {
                    constant.CODE_ERR_MSG: mess,
                    constant.CODE_STATUS: constant.VALUE_FAILED
                }
                return response
            
    @staticmethod
    def get_state_submission_status(mission_id, token):
        rest = connect_sdk_flagship()
        if token is not None and rest.authenticated(token):
            try:
                mission = srv.get_mission(rest,mission_id)
                json_form = srv.get_report_data(rest, mission)
                responses = []
                l_faces = []
                qphotos = rest.com_get_mission_photos(mission)
                list_submission = get_list_submission(qphotos)         
                    
                cmpt = 0
                for ph in qphotos:
                    cmpt += 1
                    print('CMPT STATUS ',cmpt)
                    status = srv.get_status_json_data_form(json_form, ph.id)
                    if status is not None:
                        if status == 'Good' or status == "BON":
                            state = 'BON'
                        elif status == 'Low Degradation' or status == "FAIBLE DEGRADATION":
                            state = 'FAIBLE DEGRADATION'
                        elif status == 'Strong degradation' or status == "FORTE DEGRADATION":
                            state = 'FORTE DEGRADATION'
                        elif status == 'Critical' or status == "CRITIQUE":
                            state = 'CRITIQUE'
                        elif status == 'NOT TREATED' or status == "NON TRAITÉE" or status == "" or status == "NON TRAITEE":
                            state = 'NON TRAITEE'
                        else:
                            state = "NON TRAITEE"
                    else:
                        state = "NON TRAITEE"
                    l_faces.append(json_photo_status(ph,state))
                
                for i,submission in enumerate(list_submission):
                    name = "{}".format(submission)
                    type_submission = "{}".format(name.split(' ')[0]).lower()
                    missions = [x for x in l_faces if x['submission'] == list_submission[i]]
                    format_response = format_response_subm(name,missions,type_submission)
                    responses.append(format_response)
                return responses           
                
            except QualiticsFlagshipException as ex:
                mess = "/ {}".format(ex).upper()
                response = {
                    constant.CODE_ERR_MSG: mess,
                    constant.CODE_STATUS: constant.VALUE_FAILED
                }
                return response
            
        
def format_response_subm(submission,missions,types):
    name = "{}".format(submission)
    if name.split(' ')[0] == 'Arête':
        s = 'Arete {}'.format(name.split(' ')[1])
        photo_response = {
            constant.KEY_FACE: s,
            constant.KEY_MISSION: missions,
            constant.KEY_STATUS: "",
            'type': 'arete'
        }
    else:
        photo_response = {
            constant.KEY_FACE: name,
            constant.KEY_MISSION: missions,
            constant.KEY_STATUS: "",
            'type': types
        }

    return photo_response


def format_respose_statut(submission, status_list):
    name = "{}".format(submission)
    if name.split(' ')[0] == 'Arête':
        s = 'Arete {}'.format(name.split(' ')[1])
        response = {
            constant.KEY_FACE: s,
            constant.KEY_STATE: srv.format_state(status_list)
        }
    else:
        response = {
            constant.KEY_FACE: name,
            constant.KEY_STATE: srv.format_state(status_list)
        }

    return response


def get_list_submission(qphotos):
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

    return ls_ordered


def get_list_status(subm_list):
    init_List = []
    for subm in subm_list:
        init_List.append(subm['status'])
    return init_List
