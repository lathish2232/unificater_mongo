import os

from django.http import JsonResponse
from rest_framework import status
from platform import system

from service.util.unify_response import validation_error_response,internal_server_response
from service.util.unify_logger import UNIFY_ERROR, unify_printer

def process_folder_structure(request):
    try:
        if system().lower()=='windows':
            home_path=os.path.expanduser("~").replace("\\","/")
        else:
            home_path = '/home'
        records = {'code': 200, 'message': 'Success', 'data': {'baseDir': None, 'files': []}}
        slno = 1
        if request.data:
            dir = request.data['value']
            if os.path.isdir(dir):
                os.chdir(dir)
                for rec in os.listdir(dir):
                    if not rec.startswith('.'):
                        currFile = os.path.join(os.getcwd(), rec).replace("\\", "/")
                        records['data']['files'].append({'id': slno, 'value': currFile, 'isDir': os.path.isdir(currFile)})
                    slno += 1
            else:
                response = validation_error_response(f"{dir} is not correct path, please provide check it")
                return JsonResponse(validation_error_response(response), status=status.HTTP_400_BAD_REQUEST)
        else:
            os.chdir(home_path)
            for rec in os.listdir(os.getcwd()):
                if not rec.startswith('.'):
                    currFile = os.path.join(os.getcwd(), rec).replace("\\", "/")
                    records['data']['files'].append({'id': slno, 'value': currFile, 'isDir': os.path.isdir(currFile)})
                    slno += 1
        records['data']['baseDir'] = home_path
        return JsonResponse(records, status=status.HTTP_200_OK)
    except Exception as ex:
        message = 'Error occurred  While getting folder and files information, make sure u have proper Permission'
        unify_printer(level=UNIFY_ERROR, message=message,
                          error=ex, traceback=traceback.format_exc())
        return JsonResponse(internal_server_response(message, traceback=traceback.format_exc()),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
