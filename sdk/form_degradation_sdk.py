from flagshipcore.flagship.libserver import QualiticsFlagship, QualiticsFlagshipException
import _pickle as pickle
from flask import current_app, json
from utils.constants import Constant as constant
import uuid
from .services import Service as srv, search_data_form
from _dbus_bindings import String
from .form_sdk import FormSDK as f


def connect_sdk_flagship():
    return QualiticsFlagship(current_app.config['FLAGSHIP_SERVER'])


class FormDegradation(object):

    @staticmethod
    def save_or_update(token, mission_id, photo_id, form_request):
        rest = connect_sdk_flagship()

        if token is not None and rest.authenticated(token):
            try:
                mission = srv.get_mission(rest, mission_id)
                report_data = srv.get_report_data(rest, mission)
                #print("REPORT DATA : ",report_data)
                photo_info = srv.get_photo_info(rest, mission, photo_id)
                print('REPORT DATA', report_data)
                data = search_data_form(report_data, String(photo_id))
                print('DATAAAAAAAAA : ', data)
                # Création de Formulaire de Sauvegarde
                print('FORMMMMMMMMMM_________REQUESTTTTTTTTTTT : ', form_request)
                form = format_degradation(form_request)
                print('FORMMMMMMMMMM_________REQUESTTTTTTTTTTT FORMATTT: ', form)
                updated_data = update_form_degradation(data, form)
                print('UPDATED LISTTTTTTTTTTTTTTTTTTTTTTTTT : ', updated_data)
                if updated_data is None:
                    formatage_data = srv.format_data_report(data, report_degradation=form, id=photo_id)
                    data_save_or_update = srv.update_report_data(report_data, formatage_data)
                    rest.adm_set_report_data(mission, data_save_or_update)
                    response = {
                        constant.CODE_STATUS: constant.VALUE_SUCCESS,
                        constant.CODE_SUC_MSG: constant.TEXT_FORM_SAVE_SUCCESS,
                        'data': data_save_or_update
                    }
                else:
                    formatage_data = srv.format_data_report(data, report_degradation=updated_data)
                    data_save_or_update = srv.update_report_data(report_data, formatage_data)
                    print('DATA SAVE OR UPDATE : ', data_save_or_update)
                    rest.adm_set_report_data(mission, data_save_or_update)
                    response = {
                        constant.CODE_STATUS: constant.VALUE_SUCCESS,
                        constant.CODE_SUC_MSG: constant.TEXT_FORM_SAVE_SUCCESS,
                        'data': data_save_or_update
                    }

                    return constant.TEXT_FORM_SAVE_SUCCESS

            except QualiticsFlagshipException as ex:
                mess = "/ {}".format(ex).upper()
                return mess

    @staticmethod
    def get_report_degradation(token, mission_id, photo_id):
        rest = connect_sdk_flagship()
        list_v = []

        if token is not None and rest.authenticated(token):
            try:
                mission = srv.get_mission(rest, mission_id)
                photo_info = srv.get_photo_info(rest, mission, photo_id)
                report_data_1 = srv.get_report_data(rest, mission)
                data1 = search_data_form(report_data_1, String(photo_info.id))
                print('REPORT DATA ::::::::::::::', data1)

                if data1 == None:
                    data = {
                        'id': photo_id,
                        'status': 'NOT TREATED',
                        'description': '',
                        'form_dis': []
                    }
                    print('SAVEEEEE ', f.save_report_data(token, data, mission_id=mission_id))

                report_data = srv.get_report_data(rest, mission)
                print('REPORT DATA :: ', report_data)
                data = search_data_form(report_data, String(photo_info.id))
                print('SEARCH DATA ::: ', data)
                item = get_form_degradation(data)
                print('ITEMMMM ::: ', item)
                #it = search_data_form(report_data,String(photo_info.id))
                if item is None:
                    return list_v
                else:
                    print("RESPONSE FFF11111:::: ", item['coordinates'])
                    response = {
                        'geojson': item['coordinates'],
                    }
                    print("RESPONSE :::: ", item['coordinates'])
                    json_string = json.dumps(item['coordinates'])
                    data = json.loads(json_string)
                    print('DATTTTTTTAAAAAAAAAAAAAAAA ::::: ', data)
                    return data
            except QualiticsFlagshipException as ex:
                mess = "/ {}".format(ex).upper()
                return mess


def random_uuid() -> str:
    id = uuid.uuid4()
    print("The id generated using uuid4() : ", end="")
    print(id)

    print("int Representation : ", end="")
    print(id.int)

    print("hex Representation : ", end="")
    print(id.hex)
    r_value = str(id)
    return r_value


def format_degradation(form):
    print('REPORT FORMMMMMMMMMM ::: ', form)
    ''' id_g_request = form.get('random_id','') '''
    r_uuid = random_uuid()
    ''' if id_g_request == '':
        random_id = r_uuid '''
    ''' else:
        if form.get('random_id',''):
            random_id = form['random_id'] '''
    # meta_data ajout langue
    # form_data
    res = {
        'random_id': r_uuid,
        'coordinates': form
    }
    ''' if form.get('status','') == '':
        res = {
        'random_id': r_uuid,
        'status': "",
        'description': "",
        'coordinates': form,
        'langue': ""
        }
    else:
        res = {
            'random_id': r_uuid,
            'status': form['status'],
            'description': form['description'],
            'coordinates': form,
            'langue': ""
        } '''

    return res


def get_form_degradation(data):
    if data is None:
        print('REPORT DATA NONE : (get_form_degradation) ')
        return None
    elif data is not None:
        form_dis = data.get('form_dis', '')
        print('FORMMMMMM DISSSS ', form_dis)
        if form_dis == '':
            return None
        elif len(form_dis) > 0:
            for i, item in enumerate(form_dis):
                if item == "NOT IMPLEMENTED":
                    form_dis.pop(i)
                    pass
                else:
                    return item
                    print('ITEMMMMMM ::: ', item)
                    ''' if len(form_dis) == 1:
                        if random_id is not None and random_id == item['random_id']:
                            return item
                        else:
                            return None                                         
                    elif len(form_dis) > 1:
                        if random_id is not None and random_id == item['random_id']:
                            return item '''

            return None
        else:
            return None
    else:
        print('REPORT DATA NONE ( #### get_form_degradation ####)')
        return None


def update_form_degradation(data, form):
    #data = search_data_form(report_data,String(photo_info.id))
    init_List = []

    if data is None:
        print('REPORT DATA NONE : (update_form_degradation) ')
        return None
    elif data is not None:
        print(data)
        form_dis = data.get('form_dis', '')
        print("Form disssssssss", form_dis)

        if form_dis is None:
            init_List.append(form)
            return init_List

        if form_dis == '':
            return None

        if len(form_dis) == 0:
            if form is not None:
                init_List.append(form)
            return init_List
        elif len(form_dis) > 0:
            print(form_dis)
            for i, item in enumerate(form_dis):
                if len(form_dis) == 1:
                    if item == "NOT IMPLEMENTED" and form is not None:
                        init_List.append(form)
                        return init_List
                    elif form is not None:
                        if item['random_id'] == form['random_id']:
                            form_dis[i] = form
                            return form_dis
                        else:
                            form_dis.append(form)
                            return form_dis
                        form_dis.append(form)
                    else:
                        return init_List
                elif len(form_dis) > 1:
                    print("RANDOM_IDDDDDDDDDD : ", form['random_id'])
                    print("RANDOM ITEM IDDDDDDDDD : ", item)
                    if item == "NOT IMPLEMENTED" and form is not None:
                        init_List.append(form)
                        form_dis.pop(i)
                        pass
                    elif item is not "NOT IMPLEMENTED" and form is not None:
                        form_dis[i] = form
                        return form_dis
                        ''' if item['random_id'] == form['random_id']:
                            form_dis[i] = form
                            return form_dis '''
            if form is not None:
                form_dis.append(form)
                return form_dis
        else:
            return init_List
    else:
        print('UPDATED FORM DEGRADATION NONE : (update_form_degradation) ')
        return None
