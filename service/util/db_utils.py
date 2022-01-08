import os
import traceback

import mysql.connector
import psycopg2
import pyodbc
from pymongo import MongoClient

from django.http import JsonResponse
from rest_framework import status
from service.util.unify_response import internal_server_response

from service.util.json_utils import extract_sub_json, get_flow_by_name

from service.util.unify_logger import unify_printer, UNIFY_ERROR
from unificater.settings import DATABASE, DB_HOST, DB_PORT, IS_AUTH_ENABLE, AUTH_DB, AUTH_DB_USER, AUTH_DB_PASS
from users.UserDetails import UserDetails
from service.util.json_utils import get_mongod_connection

FLOW_DB = DATABASE


# def get_mongod_connection(db=FLOW_DB):
#     client = None
#     try:
#         if not UserDetails.FLOW_MONGO_CONNECTION:
#             unify_printer(message='Creating FLow MongoDB client connection')
#             CONN_STR = f'mongodb://{DB_HOST}:{DB_PORT}'
#             DATABASE_NAME = db
#             client = MongoClient(CONN_STR)
#             if IS_AUTH_ENABLE:
#                 client[AUTH_DB].authenticate(AUTH_DB_USER, AUTH_DB_PASS)
#             UserDetails.FLOW_MONGO_CONNECTION = client[DATABASE_NAME]
#     except Exception as ex:
#         unify_printer(level=UNIFY_ERROR, message='Exception occurred while connection Mongo database', error=ex,
#                       traceback=traceback.format_exc())
#         raise Exception(ex)
#     finally:
#         if client:
#             unify_printer(message='Flow MongoDB client connection closed')
#             client.close()
#     return UserDetails.FLOW_MONGO_CONNECTION


def get_db_connection(db_name, host, port, user, password, database):
    connection = None
    try:
        unify_printer(message=f"Connecting to '{db_name}' database")
        unify_printer(message=
                      f'db_name: {db_name} | host: {host} | port: {port} | user: {user} | password: {password} | database: {database}')
        if db_name.upper() == 'postgreSql'.upper() or db_name.upper() == 'postgres'.upper():
            if database is None: database = 'postgres'
            if port:
                connect_str = f"user='{user}' host='{host}' password='{password}' port='{port}' dbname='{database}'"
            else:
                connect_str = f"user='{user}' host='{host}' password='{password}' dbname='{database}'"
            connection = psycopg2.connect(connect_str)
        elif db_name.upper() == 'MYSQL':
            if database is None: database = 'mysql'
            if port:
                connection = mysql.connector.connect(host=host, port=port, user=user, password=password, database=database)
            else:
                connection = mysql.connector.connect(host=host, user=user, password=password, database=database)
        elif db_name.upper() == 'MSSQL':
            driver = pyodbc.drivers()[0]
            if port:
                connection = pyodbc.connect(driver=driver,host=host,port=port,database=database,user=user, password=password)
            else:
                connection = pyodbc.connect(driver=driver,host=host,database=database,user=user, password=password)
        else:
            pass
            unify_printer(level=UNIFY_ERROR, message='Invalid db: {db_name}')
        return connection
    except Exception as ex:
        message = f'Excption occurred while connect {db_name} connection'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return json_response
    


def close_db_connection(connection, db_name='DB'):
    try:
        if connection:
            connection.close()
            unify_printer(message=f"{db_name} Connection closed")
    except Exception as ex:
        message = f'Excption occurred while connect {db_name} connection'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return json_response


def get_data_from_dataSource(collection, url):
    try:
        mongo_db = get_mongod_connection()
        record = mongo_db[collection].find_one({}, {'_id': 0})
        data = extract_sub_json(url, record)[3]
        return data
    except Exception as ex:
        message = f'Excption occurred while get_data_from_dataSource'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return json_response

def get_data_from_targetTypes(collection, url):
    try:
        mongo_db = get_mongod_connection()
        record = mongo_db[collection].find_one({}, {'_id': 0})
        data = extract_sub_json(url, record)[3]
        return data
    except Exception as ex:
        message = f'Excption occurred while get_data_from_targetTypes'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return json_response



def get_conn_parameters(inst_results):
    try:
        port = None
        for param in inst_results:
            if param['fieldName'] == 'hostAddress':
                host = param['userValue']
            elif param['fieldName'] == 'portNo':
                port = param['userValue']
            elif param['fieldName'] == 'userName':
                user = param['userValue']
            elif param['fieldName'] == 'password':
                password = param['userValue']
            elif param['fieldName'] == 'database':
                database = param['userValue']
            elif param['fieldName'] == 'instanceName':
                instanceName = param['userValue']
            else:
                pass
                unify_printer(level=UNIFY_ERROR, message=f'Invalid connection parameter: {param["fieldName"]}')
        return host, port, user, password, database, instanceName
    except Exception as ex:
        message = f'Excption occurred while get_data_from_targetTypes'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return json_response
    


def get_query_parameters(data_inst_result):
    try:
        query = data_inst_result.get('query')
        schema = data_inst_result.get('schema')
        return query, schema
    except Exception as ex:
        message = f'Excption occurred while get_data_from_targetTypes'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return json_response
    


def connection_str(instance_id, instances):
    conn_str = None
    try:
        for instance in instances:
            if instance['type'] == 'database':
                if instance.get('id') == instance_id:
                    for param in instance['connectionParameters']:
                        if param['fieldName'] == 'hostAddress':
                            host = param['userValue']
                        elif param['fieldName'] == 'userName':
                            user = param['userValue']
                        elif param['fieldName'] == 'password':
                            password = param['userValue']
                        elif param['fieldName'] == 'database':
                            database = param['userValue']
                        elif param['fieldName'] == 'portNo':
                            port = param['userValue']
                    if instance['name'] == 'postgreSql':
                        if port:
                            conn_str = f"postgres://{user}:{password}@{host}:{port}/{database}"
                        else:
                            conn_str = f"postgres://{user}:{password}@{host}/{database}"
                    elif instance['name'] == 'mySql':
                        if port:
                            conn_str = f"mysql://{user}:{password}@{host}:{port}/{database}"
                        else:
                            conn_str = f"mysql://{user}:{password}@{host}/{database}"
                    elif instance['name'].upper() == 'MSSQL':
                        if port:
                            conn_str = f"mssql+pyodbc://{user}:{password}@{host}:{port}/{database}?driver=SQL Server"
                        else:
                            conn_str = f"mssql+pyodbc://{user}:{password}@{host}/{database}?driver=SQL Server"
        return conn_str
    except Exception as ex:
        message = f'Excption occurred while get_data_from_targetTypes'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return json_response
    
