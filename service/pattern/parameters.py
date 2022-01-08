import traceback

from django.http import JsonResponse
from rest_framework import status

from service.util.db_utils import get_data_from_dataSource
from service.util.unify_logger import unify_printer, UNIFY_ERROR
from service.util.unify_response import success_response, no_content_response, internal_server_response
from service.util.unify_uris import CONN_TYPE_ID, CONN_JSON_URI, CONN_TYPE_URI, PATTERN_ID


def get_pattern_types(type):
    try:
        unify_printer(message='Get databases')
        url_str = CONN_JSON_URI + CONN_TYPE_URI + '/' + CONN_TYPE_ID[type] + '/connections'
        result = get_data_from_dataSource('dataSource', url_str)
        if result:
            for rec in result:
                del rec['connectionParameters']
    except Exception as ex:
        unify_printer(level=UNIFY_ERROR, message='Exception occurred while getting databases',
                      error=ex, traceback=traceback.format_exc())
        raise Exception(ex)
    return result


def get_pattern_params(request, pattern_type):
    try:
        unify_printer(message='Get pattern connection params...')
        if pattern_type == 'csv' or pattern_type == 'text':
            url = CONN_JSON_URI + CONN_TYPE_URI + '/' + CONN_TYPE_ID.get(
                'pattern') + '/connections/' + PATTERN_ID.get(pattern_type)
            conn_params = get_data_from_dataSource('dataSource', url)
        if conn_params:
            record = [{"id": "dataInstances_1", "isFwf": False, "dataParameters": conn_params['connectionParameters']}]
            result = {'type': 'pattern', 'displayName': None, 'name': pattern_type, 'dataInstances': record}
            response = success_response(data=result)
        else:
            response = no_content_response()
        json_response = JsonResponse(response, status=status.HTTP_200_OK)
    except Exception as ex:
        message = 'Exception occurred while getting database connection params'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return json_response


def get_pattern(type):
    try:
        unify_printer(message='Get databases')
        url_str = CONN_JSON_URI + CONN_TYPE_URI + '/' + CONN_TYPE_ID[type] + '/connections'
        result = get_data_from_dataSource('dataSource', url_str)
        if result:
            for rec in result:
                record = {"dataInstances": [
                    {"id": "dataInstances_1", "isFwf": False, "dataParameters": rec['connectionParameters']}]}
                rec.update(record)
                del rec['connectionParameters']
    except Exception as ex:
        unify_printer(level=UNIFY_ERROR, message='Exception occurred while getting databases', error=ex,
                      traceback=traceback.format_exc())
        raise Exception(ex)
    return result
