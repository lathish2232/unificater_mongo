from datetime import datetime

from service.util.http_constances import timeout, success_msg, no_data, internal_err_msg, duplicate_msg, construction


def success_response(message=success_msg, data=None):
    if data:
        if not isinstance(data, list):
            data = [data]
        return {"code": 200, "message": message, "data": data}
    else:
        return {"code": 204, "message": message}


def success_response_v1(message=success_msg, data=None):
    if data:
        if not isinstance(data, list):
            data = [data]
        return {"code": 200, "message": message, "data": data}
    else:
        return {"code": 200, "message": message}


def success_create_response(message, data=None):
    if data:
        if not isinstance(data, list):
            data = [data]
        return {"code": 201, "message": message, "data": data}
    else:
        return {"code": 201, "message": no_data}


def create_response(message, data=None):
    if data:
        if not isinstance(data, list):
            data = [data]
        return {"code": 201, "message": message, "data": data}
    else:
        return {"code": 201, "message": message}


def success_delete_response(message, data=None):
    if data:
        if not isinstance(data, list):
            data = [data]
        return {"code": 202, "message": message, "data": data}
    else:
        return {"code": 202, "message": message}


def no_content_response(message=no_data):
    return {"code": 204, "message": message}


def duplicate_data_response(message=duplicate_msg, data=None):
    if data:
        if not isinstance(data, list):
            data = [data]
        return {"code": 304, "message": message, "data": data}
    else:
        return {"code": 304, "message": message}


def validation_error_response(message):
    return {"code": 400, "message": message}


def not_accepted_response(message):
    return {"code": 406, "message": message}


def forbidden_response(message):
    return {"code": 403, "message": message}


def time_out_response(message=timeout):
    return {"code": 408, "message": message}


def duplicate_content_response(message):
    return {"code": 409, "message": message}


def internal_server_response(message=internal_err_msg, traceback=None):
    str_traceback = None
    if traceback:
        str_traceback = str(traceback)
    return {"code": 500, "message": message, "error": str_traceback}


def service_not_available_response(message=construction):
    return {"code": 503, "message": message}


def unauthorized(error, data=None):
    if data:
        if not isinstance(data, list):
            data = [data]
        return {"code": 401, "message": error, "data": data}
    else:
        return {"code": 401, "message": error}


def service_unavailable(error):
    return {"code": 503, "message": error}
