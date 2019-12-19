from flagshipcore.flagship.libserver import QualiticsFlagshipException
from utils.constants import Constant as constant
from flask import json


from _dbus_bindings import String
from schemas.form_schema import init_report_data, format_get_data, format_report_data


class Service(object):

    def __init__(self):
        pass

    @staticmethod
    def form_schema(jsc):
        schema = {
            constant.CODE_ID: String(jsc.id),
            'schema': jsc.schema,
            'uischema': String(jsc.uischema)
        }
        return schema

    @staticmethod
    def get_mission(rest, mission_id):
        missions = rest.adm_get_missions()
        mission = [m for m in missions if m.id == int(mission_id)][0]
        print("RECUPERATION D'UNE MISSION :::  ID == ", mission_id)
        return mission

    @staticmethod
    def get_report_data(rest, mission):
        try:
            report_data = rest.adm_get_report_data(mission).data
            if report_data is not None:
                if len(report_data) == 0:
                    return None
                if len(report_data) > 0:
                    return report_data
            else:
                return None

        except QualiticsFlagshipException as ex:
            error_msg = "GET REPORT DATA NULL : {} ".format(ex)
            print(error_msg)
            return None
        return report_data

    @staticmethod
    def format_data_report(data, report_degradation='DEFAULT', id='DEFAULT'):
        if data == None:
            form_dis = report_degradation
            form = {
                constant.CODE_ID: id,
                constant.CODE_STATUS: "NON TRAITEE",
                constant.CODE_DESCRIPTION: "ZZZZZZZZZZZ",
                'form_dis': form_dis
            }
            return form

        if data.get('description', '') == '':
            desc = ""
        else:
            desc = data['description']

        status = data.get('status', '')
        if status == '':
            stat = data.get('statut', '')
        else:
            stat = status

        if report_degradation == 'DEFAULT':
            form_dis = data.get('form_dis', '')
            if form_dis == '':
                form_dis = ["NOT IMPLEMENTED"]
            else:
                form_dis = form_dis
        else:
            form_dis = report_degradation

        print('###################### STATUSSSSSSSSSSSSSS', stat)
        form = {
            constant.CODE_ID: data['id'],
            constant.CODE_STATUS: stat,
            constant.CODE_DESCRIPTION: desc,
            'form_dis': form_dis
        }
        return form

    @staticmethod
    def update_report_data(data, form_data):
        init_List = []
        photo_id = form_data['id']
        if data is None:
            print("data", data)
            if form_data is not None:
                init_List.append(form_data)
                return init_List

        if data is not None:
            print("LENGHTS DATA FORM : ", len(data))
            print("data", data)
            if len(data) == 0:
                if form_data is not None:
                    init_List.append(form_data)
                return init_List
            elif len(data) > 0:
                for i, item in enumerate(data):
                    if photo_id == item['id']:
                        data[i] = form_data
                        return data
                if form_data is not None:
                    data.append(form_data)
                    return data
            else:
                return init_List

    @staticmethod
    def clean_report_data(data, form_data):
        init_List = []
        return init_List

    @staticmethod
    def get_photo_info(rest, mission, id_photo):
        qphotos = rest.com_get_mission_photos(mission)
        photo_info = [photo for photo in qphotos if photo.id == int(id_photo)][0]
        return photo_info

    @staticmethod
    def verif_id_photo(rest, mission, id_photo):
        qphotos = rest.com_get_mission_photos(mission)
        photo_info = [photo for photo in qphotos if photo.id == int(id_photo)][0]

        if photo_info.id == int(id_photo):
            print("VERIFICATION DU MISSION SUCCESS !!!")
            return True

        return False

    @staticmethod
    def get_status_json_data_form(json_form, photo_id):

        #print("JSON FORM ", json_form)
        if json_form is None:
            return None
        else:
            item = search_data_form(json_form, String(photo_id))
            if item is not None:
                status = item['status']
            else:
                status = None
            return status

    @staticmethod
    def format_state(count_status):
        cmp_b, cmp_f, cmp_fo, cmp_c, cmp_n = get_count_status(count_status)
        response_stat = {
            constant.VALUE_T_B: cmp_b,
            constant.VALUE_T_FA: cmp_f,
            constant.VALUE_T_FO: cmp_fo,
            constant.VALUE_T_C: cmp_c,
            constant.VALUE_T_NT: cmp_n
        }
        return response_stat


def get_count_status(status_list):
    cmp_b = 0
    cmp_f = 0
    cmp_fo = 0
    cmp_c = 0
    cmp_n = 0

    for l_stat in status_list:
        if l_stat == "BON" or l_stat == "Good":
            cmp_b += 1
        if l_stat == "FAIBLE DEGRADATION" or l_stat == "Low Degradation":
            cmp_f += 1
        if l_stat == "FORTE DEGRADATION" or l_stat == "Strong degradation":
            cmp_fo += 1
        if l_stat == "CRITIQUE" or l_stat == "Critical":
            cmp_c += 1
        if l_stat == "NON TRAITEE" or l_stat == "statut" or l_stat == "NORMAL" or l_stat == "NOT TREATED" or l_stat == "" or l_stat == "NON TRAITÉE":
            cmp_n += 1

    return cmp_b, cmp_f, cmp_fo, cmp_c, cmp_n


def search_data_form(data, id):
    print("LENGTH ITEMS: ", len(data))
    if data is None:
        return None

    if data is not None:
        if len(data) == 0:
            return None
        if len(data) > 0:
            for i, item in enumerate(data):
                if len(data) == 1:
                    if id == item['id']:
                        return item
                    else:
                        return None
                elif len(data) > 1:
                    if id == item['id']:
                        return item
        else:
            return None

    return None


def get_json_langue(data):
    test_list = []
    statu = data['status']
    test_list.append(statu)
    print(test_list)

    status = ["Good", "Low Degradation", "Strong degradation", "Critical", "NOT TREATED"]
    statut = ["BON", "FAIBLE DEGRADATION", "FORTE DEGRADATION", "CRITIQUE", "NON TRAITÉE"]

    resFR = all(ele in statut for ele in test_list)
    resEN = all(ele in status for ele in test_list)

    if len(test_list) > 0:
        if resFR is True:
            FR = {
                "description": data['description'],
                "statut": statu
            }
            for i, st in enumerate(statut):
                if st == statu:
                    stEN = status[i]
                    EN = {
                        "description": data['description'],
                        "status": stEN
                    }
                    response = {
                        'FR': FR,
                        'EN': EN
                    }
                    return response

        if resEN is True:
            EN = {
                "description": data['description'],
                "status": data['status']
            }
            for i, st in enumerate(status):
                if st == statu:
                    stFR = statut[i]
                    FR = {
                        "description": data['description'],
                        "statut": stFR
                    }
                    response = {
                        'FR': FR,
                        'EN': EN
                    }
                    return response

        if resFR is False and resEN is False:
            FR = {
                "description": data['description'],
                "statut": "NON TRAITÉE"
            }
            EN = {
                "description": data['description'],
                "status": "NOT TREATED"
            }
            response = {
                'FR': FR,
                'EN': EN
            }
            return response

    else:
        FR = {
            "description": data['description'],
            "statut": "NON TRAITÉE"
        }
        EN = {
            "description": data['description'],
            "status": "NOT TREATED"
        }
        response = {
            'FR': FR,
            'EN': EN
        }
        return response
