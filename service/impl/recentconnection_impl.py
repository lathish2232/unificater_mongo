import mysql.connector
import psycopg2
from django.http import JsonResponse
from mysql.connector.errors import InterfaceError, ProgrammingError, DatabaseError
from psycopg2 import OperationalError
from rest_framework import status
from rest_framework.status import HTTP_202_ACCEPTED

from service.impl.main_uniflow import insertMasterJsonItems
from service.util.db_utils import get_mongod_connection
from service.util.json_utils import extract_sub_json, get_flow_by_name, update_flow_by_name
from service.util.unify_logger import unify_printer
from service.util.unify_response import no_content_response, success_response, unauthorized, success_delete_response


def recentconn_create_instance(request, flow):
    d = {'id': None}
    displayName = request.data['displayName']
    flow_db = get_mongod_connection()
    recent_conn = flow_db.recentConnections.find_one({'displayName': displayName}, {'_id': 0})
    record = get_flow_by_name(flow)
    url = '/' + flow + '/instances'
    # instance_id
    insId = [int(i['id'].split('_')[-1]) for i in record[flow]['instances']]
    d['id'] = 'instanceId_' + str(1 if len(insId) <= 0 else max(insId) + 1)
    recent_conn.update(d)
    _, keys, _, json = extract_sub_json(url, record)

    for param in recent_conn['connectionParameters']:
        if param['fieldName'] == 'hostAddress':
            host = param['userValue']
        elif param['fieldName'] == 'userName':
            user = param['userValue']
        elif param['fieldName'] == 'password':
            password = param['userValue']
        elif param['fieldName'] == 'database':
            db = param['userValue']
        elif param['fieldName'] == 'portNo':
            port = param['userValue']
    dbtype = recent_conn['name']
    if dbtype == 'postgreSql' or dbtype.upper() == 'postgres'.upper():
        try:
            if port:
                connect_str = f"host='{host}' user='{user}' password='{password}' dbname='{db}' port='{port}'"
            else:
                connect_str = f"host='{host}' user='{user}' password='{password}' dbname='{db}'"
            connection = psycopg2.connect(connect_str)
            connection.close()
        except OperationalError as error:
            return JsonResponse(unauthorized(error=str(error).rstrip()), status=status.HTTP_401_UNAUTHORIZED)
    elif dbtype == 'mySql':
        try:
            if port:
                connection = mysql.connector.connect(host=host, port=port, user=user, password=password)
            else:
                connection = mysql.connector.connect(host=host, user=user, password=password)
            connection.close()
        except (InterfaceError, ProgrammingError, DatabaseError) as error:
            return JsonResponse(unauthorized(error=str(error).rstrip()), status=status.HTTP_401_UNAUTHORIZED)

    insertMasterJsonItems(record, keys, 0, recent_conn)
    data = update_flow_by_name(flow, record)
    return JsonResponse(success_response(data=data), status=status.HTTP_200_OK)


def get_recent_connections(request):
    flow_db = get_mongod_connection()
    if request.method == 'GET':
        unify_printer(message='Get recent connections')
        result = []
        record = [row for row in flow_db.recentConnections.find({}, {'_id': 0})]
        if record:
            for rows in record:
                result.append({'displayName': rows['displayName']})
        else:
            return JsonResponse(no_content_response(message='Saved database connections not available'),
                                status=status.HTTP_200_OK)
    elif request.method == 'POST':
        if request.data:
            displayName = request.data['displayName']
            result = flow_db.recentConnections.find_one({'displayName': displayName}, {'_id': 0})
    return JsonResponse(success_response(data=result), status=status.HTTP_200_OK)


def del_recent_connections(request):
    displayName = request.data['displayName']
    flow_db = get_mongod_connection()
    record = flow_db.recentConnections.find_one({'displayName': displayName}, {'_id': 0})
    if record:
        flow_db.recentConnections.delete_one({'displayName': displayName})
        return JsonResponse(success_delete_response(message=f'{displayName} connection has been deleted successfully'),
                            status=status.HTTP_200_OK)
    else:
        return JsonResponse(no_content_response(), status=status.HTTP_200_OK)


def update_recent_connectins(request):
    pass
