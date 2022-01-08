import json
import logging
import time
import traceback

import sqlvalidator
from django.http import JsonResponse
from pandas import DataFrame
from pymongo.errors import ServerSelectionTimeoutError
from rest_framework import status

from service.impl import mssql, postgres
from service.impl.mssql.processor import process_mssql_query
from service.impl.mysql.processor import process_mysql_query
from service.impl.postgres.processor import process_postgres_query
#from service.impl.refpkg.cache import clear_all_cached_functions, clearable_lru_cache
from service.util.db_utils import get_conn_parameters, get_query_parameters
from service.util.db_utils import get_data_from_dataSource
from service.util.http_constances import invalid_query, invalid_input
from service.util.json_utils import extract_sub_json, parse_meta_data_search_input, get_flow_by_name, \
    update_flow_by_name
from service.util.unify_logger import unify_printer, UNIFY_ERROR
from service.util.unify_response import success_response, time_out_response, internal_server_response, \
    no_content_response, success_create_response, validation_error_response, \
    not_accepted_response
from service.util.unify_uris import CONN_TYPE_ID, DATABASE_ID


def get_db_connection_types(request, url_path):
    try:
        unify_printer(message='Get databases connection params...')
        url_ends = url_path.split('/')[-1]
        if url_ends == 'postgreSql' or url_ends.upper() == 'postgres'.upper() or url_ends.upper() == 'MSSQL' or url_ends == 'mySql':
            url = '/connectionJson/connectionTypes/' + CONN_TYPE_ID.get(
                'database') + '/connections/' + DATABASE_ID.get(url_ends)  # + '/connectionParameters'
            conn_params = get_data_from_dataSource('dataSource', url)
        if conn_params:
            result = {'type': 'database', 'displayName': None, 'name': url_ends,
                      'connectionParameters': conn_params['connectionParameters'], 'dataInstances': []}
            response = success_response(data=result)
        else:
            response = no_content_response()
        json_response = JsonResponse(response, status=status.HTTP_200_OK)
    except ServerSelectionTimeoutError as tex:
        unify_printer(level=UNIFY_ERROR, message='Server Timeout occurred while getting database connection params',
                      error=tex, traceback=traceback.format_exc())
        response = time_out_response()
        json_response = JsonResponse(response, status=status.HTTP_408_REQUEST_TIMEOUT)
    except Exception as ex:
        message = 'Exception occurred while getting database connection params'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return json_response


#@clearable_lru_cache()
def fetch_data_from_db(db_name, host, port, user, password, query, database, schema):
    if db_name == 'postgreSql' or db_name.upper() == 'postgres'.upper():
        result: DataFrame = process_postgres_query(db_name, host, port, user, password, query, database,
                                                   schema)
    elif db_name == 'mySql':
        result: DataFrame = process_mysql_query(db_name, host, port, user, password, query, database)
    elif db_name.upper() == 'MSSQL':
        result: DataFrame = process_mssql_query(db_name, host, port, user, password, query, database)
    return result


def process_data_instance(request, flow, instance_id, data_instance_id=None, is_exc=False):
    try:
        record = get_flow_by_name(flow)
        if request.method == 'GET' and is_exc:
            inst_result = \
                extract_sub_json(request.path.replace(f'/dataInstances/{data_instance_id}/exc', ''), record)[3]
            conn_params = extract_sub_json('/connectionParameters', inst_result)[3]
            data_inst_result = extract_sub_json(request.path.replace('/exc', ''), record)[3]
            if inst_result and conn_params and data_inst_result:
                db_name = inst_result['name']
                host, port, user, password, database, instanceName = get_conn_parameters(conn_params)
                query, schema = get_query_parameters(data_inst_result)
                unify_printer(message=f'dn_name: {db_name}')
                unify_printer(message=f'query: {query} | schema: {schema}')
                unify_printer(
                    message=f'host: {host} | port: {port} | user: {user} | password: {password} | database: {database}')
                # if db_name == 'postgreSql' or db_name.upper() == 'postgres'.upper():
                #     result: DataFrame = process_postgres_query(db_name, host, port, user, password, query, database,
                #                                                schema)
                # elif db_name == 'mySql':
                #     result: DataFrame = process_mysql_query(db_name, host, port, user, password, query, database)
                # elif db_name.upper() == 'MSSQL':
                #     result: DataFrame = process_mssql_query(db_name, host, port, user, password, query, database)
                result = fetch_data_from_db(db_name, host, port, user, password, query, database, schema)
                df_json = {}
                df_json['columns'] = list(result.columns)
                if not result.empty:
                    start = None
                    end = None
                    queryRange = request.query_params.get('range', None)
                    if queryRange:
                        range = queryRange.split('-')
                        start = int(range[0])
                        end = int(range[1])

                    if start:
                        df_json['counts'] = None
                    else:
                        #clear_all_cached_functions()
                        df_json['counts'] = {'columns': result.shape[1], 'rows': result.shape[0]}
                    df_json['rows'] = json.loads(result.loc[start:end, :].to_json(orient="records", date_format='iso'))
                    response = success_response(data=df_json)
                else:
                    response = no_content_response()
            else:
                response = validation_error_response('Invalid request')
            json_response = JsonResponse(response, status=status.HTTP_200_OK)
        elif request.method == 'GET':
            result = extract_sub_json(request.path, record)[3]
            if result:
                response = success_response(data=result)
            else:
                response = no_content_response()
            json_response = JsonResponse(response, status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            inst_result = extract_sub_json(f'/{flow}/instances/{instance_id}', record)[3]
            data_inst_result = extract_sub_json(request.path, record)[3]
            body: dict = request.data
            if inst_result and data_inst_result:
                is_valid = True
                inst_type = inst_result['type']
                if inst_type.upper() == 'database'.upper():
                    if body['type'] and body['type'] == 'table':
                        body['query'] = f"SELECT * FROM {body['schema'] + '.' + body['table']}"
                    query = body['query']
                    sql_query = sqlvalidator.parse(query)
                    if sql_query.is_valid():
                        body['id'] = data_instance_id
                        data_inst_result.update(body)
                    else:
                        is_valid = False
                        unify_printer(message=f'SQL query error: {sql_query.errors}')
                        response = validation_error_response(invalid_query)
                else:
                    body['id'] = data_instance_id
                    data_inst_result.update(body)
                if is_valid:
                    result = update_flow_by_name(flow, record)
                    if result:
                        response = success_create_response(f'Data Instance updated successfully', data=result)
                    else:
                        response = not_accepted_response('Nothing modified to update')
                else:
                    json_response = JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)
                    return json_response
            else:
                response = validation_error_response(invalid_input)
            json_response = JsonResponse(response, status=status.HTTP_200_OK)
        elif request.method == 'POST':
            body: dict = request.data
            inst_result = extract_sub_json(f'/{flow}/instances/{instance_id}', record)[3]
            if inst_result:
                if inst_result['type'] and inst_result['type'].upper() == 'DATABASE' and body['type'] \
                        and body['type'] == 'table':
                    body['query'] = f"SELECT * FROM {body['schema'] + '.' + body['table']}"
                query = body['query']
                sql_query = sqlvalidator.parse(query)
                if sql_query.is_valid():
                    data_instances = extract_sub_json(request.path, record)[3]
                    num = [int(i['id'].split('_')[-1]) for i in data_instances]
                    data_instance_id = 'dataInstance_' + str(1 if len(num) <= 0 else max(num) + 1)
                    body['id'] = data_instance_id
                    data_instances.append(body)
                    result = update_flow_by_name(flow, record)
                    if result:
                        response = success_create_response(f'Data Instance created successfully', data=result)
                    else:
                        response = not_accepted_response('Nothing new to create')
                else:
                    unify_printer(message=f'SQL query error: {sql_query.errors}')
                    response = validation_error_response(invalid_query)
                    json_response = JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)
                    return json_response
            else:
                response = validation_error_response(invalid_input)
            json_response = JsonResponse(response, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            instances = record.get(flow).get('instances')
            is_exist = False
            is_del = False
            for instance in instances:
                if instance.get('id') == instance_id:
                    data_instances = instance.get('dataInstances')
                    for data_instance in data_instances:
                        if data_instance.get('id') == data_instance_id:
                            is_exist = True
                            if not data_instance.get('isActiveInFlow'):
                                is_del = True
                                data_instances.remove(data_instance)
                            break
            if is_exist:
                if is_del:
                    result = update_flow_by_name(flow, record)
                    if result:
                        response = success_create_response('Data Instance deleted successfully', data=result)
                    else:
                        response = not_accepted_response('Nothing to delete')
                else:
                    response = not_accepted_response(
                        'The data instance not deleted. Since, this used by flow. remove this from flow before delete.')
            else:
                response = no_content_response()
            json_response = JsonResponse(response, status=status.HTTP_200_OK)
    except Exception as ex:
        message = 'Exception occurred while process data instance'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return json_response


def meta_data_search(request, flow, instance_id):
    try:
        request.query_params
        record = get_flow_by_name(flow)
        if request.method == 'POST':
            inst_result = extract_sub_json(request.path.replace(f'/metasearch', ''), record)[3]
            conn_params = extract_sub_json('/connectionParameters', inst_result)[3]
            if inst_result and conn_params:
                db_name = inst_result['name']
                host, port, user, password, database, param_database = get_conn_parameters(conn_params)
                unify_printer(message=f'dn_name: {db_name}')
                unify_printer(message=f'host: {host} | port: {port} | user: {user} | password: {password}')
                body = request.data
                meta_data = parse_meta_data_search_input(body['metaData'])
                if db_name == 'postgreSql' or db_name.upper() == 'postgres'.upper():
                    result = postgres.processor.get_meta_info(meta_data, host, port, user, password)
                if db_name.upper() == 'MSSQL':
                    result = mssql.processor.get_meta_info(meta_data, host, port, user, password)
                # elif db_name == 'mySql':
                # result = process_mysql_query(db_name, host, port, user, password, query, database)
                #result=DataFrame(result)
                df_json = {}
                df_json['columns'] = list(result.columns)
                if not result.empty:
                    start = None
                    end = None
                    queryRange = request.query_params.get('range', None)
                    if queryRange:
                        range = queryRange.split('-')
                        start = int(range[0])
                        end = int(range[1])

                    if start:
                        df_json['counts'] = None
                    else:
                        df_json['counts'] = {'columns': result.shape[1], 'rows': result.shape[0]}
                    df_json['rows'] = json.loads(result.loc[start:end, :].to_json(orient="records", date_format='iso'))
                    response = success_response(data=df_json)
                else:
                    response = no_content_response()
            else:
                response = validation_error_response('Invalid request')
            json_response = JsonResponse(response, status=status.HTTP_200_OK)
    except Exception as ex:
        message = 'Exception occurred while doing metadata search'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return json_response


def process_targetdata_instance(request, flow, instance_id):
    try:
        record = get_flow_by_name(flow)
        url = f'/{flow}/instances/{instance_id}'
        ins_result = extract_sub_json(url, record)[3]
        if request.method == 'POST':
            if ins_result['id'] == instance_id:
                # trget_id function append target datainstance Id
                rec = trget_id(ins_result, request.data)
        response = success_response(data='Work in progress')
        json_response = JsonResponse(response, status=status.HTTP_200_OK)

    except Exception as ex:
        message = 'Exception occurred while doing metadata search'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return json_response


def trget_id(ins_result, request_body):
    trget_data = ins_result.get("targetDataInstances")
    if len(trget_data) >= 1:
        num = [int(i['id'].split('_')[-1]) for i in trget_data]
        id = 'dataInstance_' + str(1 if len(num) <= 0 else max(num) + 1)
    else:
        id = 'dataInstance_1'
    request_body['id'] = id
    trget_data.append(request_body)
    return trget_data
