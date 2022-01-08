import traceback

from django.http import JsonResponse
from pymongo.errors import ServerSelectionTimeoutError
from rest_framework import status

from service.util.db_utils import get_data_from_dataSource
from service.util.unify_logger import unify_printer, UNIFY_ERROR
from service.util.unify_response import success_response, time_out_response, internal_server_response
from service.util.unify_uris import CONN_TYPE_ID


def get_restapi_params(request):
    try:
        unify_printer(message='Get connection types')
        url = f'/connectionJson/connectionTypes/{CONN_TYPE_ID["restapi"]}/connections'
        result = get_data_from_dataSource('dataSource', url)
        if result:
            return JsonResponse(success_response(data=result))
    except ServerSelectionTimeoutError as tex:
        unify_printer(level=UNIFY_ERROR, message='Server Timeout occurred while getting connection types',
                      error=tex, traceback=traceback.format_exc())
        response = time_out_response()
        json_response = JsonResponse(response, status=status.HTTP_408_REQUEST_TIMEOUT)
    except Exception as ex:
        message = 'Exception occurred while getting connection types'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return json_response
