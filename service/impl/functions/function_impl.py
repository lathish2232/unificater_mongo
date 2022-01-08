from django.http import JsonResponse
from rest_framework import status
from service.util.unify_response import success_response

from service.impl.functions.function_list import functions
from service.impl.functions.display_function_list import display_functions


def parse_functions(request):
    seriesFunctions = []
    dateFunctions = []
    stringFunctions = []
    catFunctions = []
    sparseFunctions = []
    for function in functions['seriesFunctions']:
        seriesFunctions.append({'functionName': function['functionName'], 'displayName': function['displayName']})
    for function in functions['dateFunctions']:
        dateFunctions.append({'functionName': function['functionName'], 'displayName': function['displayName']})
    for function in functions['stringFunctions']:
        stringFunctions.append({'functionName': function['functionName'], 'displayName': function['displayName']})
    for function in functions['catFunctions']:
        catFunctions.append({'functionName': function['functionName'], 'displayName': function['displayName']})
    for function in functions['sparseFunctions']:
        sparseFunctions.append({'functionName': function['functionName'], 'displayName': function['displayName']})
    function = {'seriesFunctions': seriesFunctions,
                'dateFunctions': dateFunctions,
                'stringFunctions': stringFunctions,
                'catFunctions': stringFunctions,
                'sparseFunctions': sparseFunctions}
    # addIdToDict(function)
    response = JsonResponse(success_response(data=function), status=status.HTTP_200_OK)
    return response


def get_functions(request):
    response = JsonResponse(success_response(data=display_functions), status=status.HTTP_200_OK)
    return response


def get_function_on_id(request):
    f_id = request.data['id']
    fn = functions[f_id]
    response = JsonResponse(success_response(data=fn), status=status.HTTP_200_OK)
    return response


def format_function(function_payload):
    f_str = ''
    for rec in function_payload:
        functon_name = rec['functionName'][:-1]
    for dataParem in function_payload:
        if dataParem['dataParameters']:
            for parem in dataParem['dataParameters']:
                f_str += f"{parem['fieldName']}={parem['userValue']},"
            f_str.rstrip(',')
        else:
            pass
    str_function = '.' + functon_name + f_str.rstrip(',') + dataParem['functionName'][-1:]
    return str_function
