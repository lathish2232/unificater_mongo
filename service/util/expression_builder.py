import traceback

from baron import parse, dumps
from baron.path import path_to_node
from django.http import JsonResponse
from rest_framework import status

from service.impl.functions.function_impl import format_function
from service.impl.main_uniflow import updateMasterJsonItems
from service.util.json_utils import get_flow_by_name, extract_sub_json, update_flow_by_name
from service.util.unify_logger import unify_printer, UNIFY_ERROR
from service.util.unify_response import success_response, internal_server_response

operators = {'arithmeticOperators': [
    {'operator': '+', 'operatorName': 'Addition', 'example': 'x + y', 'help': None},
    {'operator': '-', 'operatorName': 'Subtraction', 'example': 'x - y', 'help': None},
    {'operator': '*', 'operatorName': 'Multiplication', 'example': 'x * y', 'help': None},
    {'operator': '/', 'operatorName': 'Division', 'example': 'x / y', 'help': None},
    {'operator': '%', 'operatorName': 'Modulus', 'example': 'x % y', 'help': None},
    {'operator': '**', 'operatorName': 'Exponentiation', 'example': 'x ** y', 'help': None},
    {'operator': '//', 'operatorName': 'Floor division', 'example': 'x // y', 'help': None}],
    'comparisonOperators': [
        {'operator': '==', 'operatorName': 'Equal', 'example': 'x == y', 'help': None},
        {'operator': '!=', 'operatorName': 'Not equal', 'example': 'x != y', 'help': None},
        {'operator': '>', 'operatorName': 'Greater than', 'example': 'x > y', 'help': None},
        {'operator': '<', 'operatorName': 'Less than', 'example': 'x < y', 'help': None},
        {'operator': '>=', 'operatorName': 'Greater than or equal to', 'example': 'x >= y', 'help': None},
        {'operator': '<=', 'operatorName': 'Less than or equal to', 'example': 'x <= y', 'help': None}],
    'logicalOperators': [
        {'operator': 'and', 'operatorName': 'AND', 'example': 'x < 5 and  x < 10',
         'help': 'Returns True if both statements are true'},
        {'operator': 'or', 'operatorName': 'OR', 'example': 'x < 5 or x < 4',
         'help': 'Returns True if one of the statements is true'},
        {'operator': 'not', 'operatorName': 'NOT ', 'example': 'not(x < 5 and x < 10)',
         'help': 'Reverse the result, returns False if the result is true'}],
    'identityOperators': [
        {'operator': 'is ', 'operatorName': 'IS', 'example': 'x is y',
         'help': 'Returns True if a sequence with the specified value is present in the object'},
        {'operator': 'is not', 'operatorName': 'Greater than or equal to', 'example': 'x is not y',
         'help': 'Returns True if both variables are not the same object'}],
    'membershipOperators': [
        {'operator': 'in', 'operatorName': 'Greater than or equal to', 'example': 'x in y',
         'help': 'Returns True if a sequence with the specified value is present in the object'},
        {'operator': 'not in', 'operatorName': 'Greater than or equal to', 'example': 'x not in y',
         'help': 'Returns True if a sequence with the specified value is not present in the object'}]
}


def process_expression(request, flow, node_id, clause_id, column_id):
    request_body = request.data
    try:
        expression = get_expression(flow, node_id, clause_id, column_id)
        exp_json = parse(request_body['expression'])
        modified_expression=""
        if request_body['requiredAction'] == 'addValue':
            modified_expression = binOpChanges(exp_json, request_body['path'], request_body['operator'],
                                                request_body['operand'])
            expression = update_expression(flow, node_id, clause_id, column_id, modified_expression)
        if request_body['update']:
            exp_json = parse(request_body['expression'])
            if request_body['requiredAction'] == 'addMethod':
                modified_expression = addMethodChanges(exp_json, request_body['path'], request_body['operand'])
                expression = update_expression(flow, node_id, clause_id, column_id, modified_expression)
            elif request_body['requiredAction'] == 'chnageOperator':
                modified_expression = changeOperator(exp_json, request_body['path'], request_body['operator'])
                expression = update_expression(flow, node_id, clause_id, column_id, modified_expression)
            elif request_body['requiredAction'] == 'binaryOperation':
                modified_expression = binOpChanges(exp_json, request_body['path'], request_body['operator'],
                                                   request_body['operand'])
                expression = update_expression(flow, node_id, clause_id, column_id, modified_expression)
        else:
            if request_body['requiredAction'] == 'addFunction':
                f_function = format_function(request_body['function'])
                modified_expression = addFunction(exp_json, request_body['path'], f_function)
                expression = update_expression(flow, node_id, clause_id, column_id, modified_expression)
        if not modified_expression:
            raise
        bornTree = addIdToDict(parse(modified_expression))
        result = {"expression": expression, "fst": bornTree}
        json_response = JsonResponse(success_response(data=result), status=status.HTTP_200_OK)
    except Exception as ex:
        message = 'Exception occurred while process expression'
        unify_printer(level=UNIFY_ERROR, message=message, error=ex,
                      traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # else:
    #     if request_body['requiedAction']=='getOperators':
    #         return get_operators(request)
    #     elif request_body['requiedAction']=='getFunction':
    #         pass
    #     elif request_body['requiedAction']=='getColumns':
    #         pass
    return json_response


# update expression in flow json


def update_expression(flow, node_id, clause_id, column_id, modified_expression):
    master_json = get_flow_by_name(flow)
    expression_path = f'/{flow}/nodes/{node_id}/data/query/clauses/{clause_id}/columns/{column_id}/expression'
    keys = extract_sub_json(expression_path, master_json)[1]
    updateMasterJsonItems(master_json, keys, modified_expression)
    update_flow_by_name(flow, master_json)
    expression = extract_sub_json(expression_path, master_json)[3]
    return expression


def get_expression(flow, node_id, clause_id, column_id):
    master_json = get_flow_by_name(flow)
    expression_path = f'/{flow}/nodes/{node_id}/data/query/clauses/{clause_id}/columns/{column_id}/expression'
    return extract_sub_json(expression_path, master_json)[3]


def get_operators(request):
    return JsonResponse(success_response(data=operators))


# Apply changes for adding binary operation
# userOption=['Column', 'Literal'], after=adding the operand before the current node or after (a=>b+a/a+b)
def binOpChanges(exprJson, path, operator, userOption, after=True):
    if exprJson: 
        curExpr = dumps(path_to_node(exprJson, path))
    else:
        curExpr = ''
        operator =''
        if not path:
            return userOption
    if after:
        path_to_node(exprJson, path[:-1])[path[-1]] = parse(curExpr + operator + userOption)
    else:
        path_to_node(exprJson, path[:-1])[path[-1]] = parse(userOption + operator + curExpr)
    return dumps(exprJson)


# Apply changes for adding binary operation
# userOption=['Column', 'Literal'], after=adding the operand before the current node or after (a=>b+a/a+b)
def changeOperator(exprJson, path, userOption):
    path_to_node(exprJson, path)[0]['value'] = userOption
    return dumps(exprJson)


# Apply changes for adding binary operation
# userOption=['function']
def addMethodChanges(ExprJson, path, userOption, params={}):
    callArgs = '('
    args = [f'{arg}={value}' for arg, value in params.items()]
    callArgs += ','.join(args)
    callArgs += ')'
    if isinstance(path[-1], int) and len(path) > 1 and path_to_node(ExprJson, path[:-2]).get('type') == 'atomtrailers':
        path_to_node(ExprJson, path[:-1])[path[-1] + 1:path[-1] + 1] = \
        parse('__UNIFDUMMY__' + '.' + userOption + callArgs)[0]['value'][1:]
    else:
        path_to_node(ExprJson, path[:-1])[path[-1]] = parse(
            dumps(path_to_node(ExprJson, path)) + '.' + userOption + callArgs)
    return dumps(ExprJson)


def addFunction(exprJson, path, format_function):
    curExpr = dumps(path_to_node(exprJson, path))
    path_to_node(exprJson, path[:-1])[path[-1]] = parse(curExpr + format_function)
    return dumps(exprJson)


def addIdToDict(obj, length=15):
    def uid(length):
        import random, string
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

    def recurse(obj):
        if isinstance(obj, list):
            for i in obj:
                recurse(i)
        elif isinstance(obj, dict) and obj:
            obj['id'] = uid(length)
            for k, v in obj.items():
                recurse(v)
    recurse(obj)
    return obj


# ------------------convert expression to Baron tree---------------------------------------------------------------
def get_baron_tree(request):
    try:
        request_body = request.data
        fst = addIdToDict(parse(request_body['expression']))
        result = {'expression': request_body['expression'], 'fst': fst}
        return JsonResponse(success_response(data=result), status=status.HTTP_200_OK)
    except Exception as ex:
        message = 'Exception occurred while get baron tree'
        unify_printer(level=UNIFY_ERROR, message=message, error=ex,
                      traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return json_response
