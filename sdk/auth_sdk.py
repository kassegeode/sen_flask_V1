from flagshipcore.flagship.libserver import QualiticsFlagship, QualiticsFlagshipException
from flask import current_app
from utils.constants import Constant as constant


def connect_sdk_flagship():
    return QualiticsFlagship(current_app.config['FLAGSHIP_SERVER'])


class AuthSdk(object):

    @staticmethod
    def login(username, password):
        rest = connect_sdk_flagship()
        try:
            if rest.authenticate(username, password):
                token = rest.get_token()
                if token is not None:
                    response = {
                        constant.KEY_USERNAME: username,
                        constant.KEY_TOKEN: token,
                        constant.CODE_STATUS: constant.VALUE_SUCCESS
                    }
                    return response
                else:
                    error_msg = "Le Token Renvoyé par le serveur est Null !!!"
                    response = {
                        constant.CODE_ERR_MSG: error_msg,
                        constant.CODE_STATUS: constant.VALUE_FAILED
                    }
                    return response
        except QualiticsFlagshipException as ex:
            mess = "/ {}".format(ex).upper()
            response = {
                constant.CODE_ERR_MSG: constant.VALUE_ERR_AUTHENTICATION + mess,
                constant.CODE_STATUS: constant.VALUE_FAILED
            }
            return response
