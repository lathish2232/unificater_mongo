import mysql.connector
import psycopg2
from django.http import JsonResponse
from mysql.connector.errors import InterfaceError, ProgrammingError, DatabaseError, OperationalError
from psycopg2 import OperationalError
from rest_framework import status

from service.impl.main_uniflow import insertMasterJsonItems
from service.util.db_utils import get_mongod_connection
from service.util.json_utils import get_flow_by_name, update_flow_by_name
from service.util.unify_response import success_response, unauthorized


class instance_db_validation():

    def __init__(self):
        pass

    def validate_db_conn(self, request_body, collection, keys, ufid):
        if request_body['type'] == 'database':
            dbtype = request_body['name']
            login_keys = [i['fieldName'].upper() for i in request_body['connectionParameters']]
            login_values = [i['userValue'] for i in request_body['connectionParameters']]
            data = dict(zip(login_keys, login_values))
            displayName = data.get('INSTANCENAME', None)
            host = data.get('HOSTADDRESS', None)
            user = data.get('USERNAME', None)
            password = data.get('PASSWORD', None)
            db = data.get('DATABASE', None)
            port = data.get('PORT NO', '')

            # service_id = data.get('SERVICE_ID', None)
            update_query = {'flowName': collection}
            if dbtype.upper() == 'POSTGRESSQL':
                try:
                    if port:
                        connect_str = f"host='{host}' user='{user}' password='{password}' dbname='{db}' port='{port}'"
                    else:
                        connect_str = f"host='{host}' user='{user}' password='{password}' dbname='{db}'"
                    connection = psycopg2.connect(connect_str)
                    connection.close()
                except OperationalError as error:
                    return JsonResponse(unauthorized(error=str(error).rstrip()), status=status.HTTP_401_UNAUTHORIZED)
            elif dbtype.upper() == 'MYSQL':
                try:
                    if port:
                        connection = mysql.connector.connect(host=host, port=port, user=user, password=password,
                                                             database=db)
                    else:
                        connection = mysql.connector.connect(host=host, user=user, password=password, database=db)
                        connection.close()
                except (InterfaceError, ProgrammingError, DatabaseError, OperationalError) as error:
                    return JsonResponse(unauthorized(error=str(error).rstrip()), status=status.HTTP_401_UNAUTHORIZED)
            else:
                pass
                # raise Exception('Invalid Input...')
            record = get_flow_by_name(collection)
            insertMasterJsonItems(record, keys, 0, request_body)
            data = update_flow_by_name(collection, record)
            # store Recent connections and flow metadata modification date
            request_body.pop('id')
            flow_db = get_mongod_connection()
            flow_db.recentConnections.update({'displayName': displayName}, {"$set": request_body}, upsert=True)
            return JsonResponse(success_response(data=data), status=status.HTTP_200_OK)
