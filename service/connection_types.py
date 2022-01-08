import json
import time
import traceback

import requests
from django.http import JsonResponse
from rest_framework import status

from service.databases.parameters import get_databases
from service.files.parameters import get_file_params
from service.pattern.parameters import get_pattern_types
from service.util.db_utils import get_data_from_dataSource
from service.util.unify_logger import unify_printer, UNIFY_ERROR
from service.util.unify_response import success_response, no_content_response, internal_server_response  # write_audit
from service.util.unify_uris import CONN_TYPE_ID, DATABASE_ID


def get_connection_types(request):
    try:
        start = time.time()
        unify_printer(message='Get connection types')
        url = '/connectionJson/connectionTypes'
        result = get_data_from_dataSource('dataSource', url)
        if result:
            for element in result:
                del element['connections']
            response = success_response(data=result)
        else:
            response = no_content_response()
        json_response = JsonResponse(response, status=status.HTTP_200_OK)
    except Exception as ex:
        message = 'Error occurred while getting connection types'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # write_audit(request, response, start, time.time())
    return json_response


def get_connection_type_property(request, type):
    try:
        start = time.time()
        if type.upper() == "DATABASE":
            result = get_databases(type)
        elif request.method == 'POST' and type.upper() == "FILE":
            result = get_file_params(request, type)
        elif type.upper() == "RESTAPI":
            result = get_url_data(request)
        elif type.upper() == 'PATTERN':
            result = get_pattern_types(type)

        if result:
            response = success_response(data=result)
        else:
            response = no_content_response()
        json_response = JsonResponse(response, status=status.HTTP_200_OK)
    except Exception as ex:
        message = 'Exception occurred while get connection properties'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # write_audit(request, response, start, time.time())
    return json_response


def get_database_parameters(request, db_name):
    try:
        start = time.time()
        unify_printer(message='Get databases connection params...')
        if db_name == 'postgreSql' or db_name.upper() == 'postgres'.upper() or db_name.upper() == 'MSSQL' or db_name == 'mySql':
            url = '/connectionJson/connectionTypes/' + CONN_TYPE_ID.get(
                'database') + '/connections/' + DATABASE_ID.get(db_name)
            conn_params = get_data_from_dataSource('dataSource', url)
        if conn_params:
            result = {'type': 'database', 'displayName': None, 'name': db_name,
                      'connectionParameters': conn_params['connectionParameters'], 'dataInstances': [],
                      'targetDataInstances': []}
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
    # write_audit(request, response, start, time.time())
    return json_response


def get_url_data(request):
    api_url = request.data.get('url', '')
    try:
        if api_url:
            url_data = requests.get(api_url)
            data = json.loads(url_data.content)
    except Exception as ex:
        unify_printer(level=UNIFY_ERROR, message='Exception occurred while get data from URL', error=ex,
                      traceback=traceback.format_exc())
        raise Exception(ex)
    return data
