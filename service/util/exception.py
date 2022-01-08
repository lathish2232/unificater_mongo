import traceback

from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import exception_handler

from service.util.unify_logger import UNIFY_ERROR, unify_printer
from service.util.unify_response import internal_server_response


def unify_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data['code'] = response.status_code

    trace = traceback.format_exc()
    message = 'Exception occurred while process request'
    unify_printer(level=UNIFY_ERROR, message=message,
                  error=exc, traceback=trace)
    res = internal_server_response(message, trace)
    response = JsonResponse(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response


def error_404(request, exception):
    message = 'The endpoint is not found'
    response = JsonResponse(data={'message': message, 'code': 404})
    response.status_code = 404
    return response


def error_500(request):
    message = 'An error occurred'
    response = JsonResponse(data={'message': message, 'code': 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    response.status_code = 500
    return response
