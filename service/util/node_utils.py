import traceback

import pandas as pd
from pandas import DataFrame
from ring import lru
from django.http import JsonResponse
from rest_framework import status
from service.util.unify_response import internal_server_response

from service.impl import query_builder as qb
from service.impl.mssql.processor import process_mssql_query
from service.impl.mysql.processor import process_mysql_query
from service.impl.postgres.processor import process_postgres_query
from service.util.db_utils import get_conn_parameters, get_query_parameters
from service.util.json_utils import extract_sub_json, get_flow_by_name
from service.util.unify_logger import unify_printer, UNIFY_ERROR


def data_instance(flow, inst_id, data_inst_id):
    try:
        flow_json = get_flow_by_name(flow)
        instances = flow_json.get(flow)['instances']
        for instance in instances:
            if instance['id'] == inst_id:
                inst_type = instance['type']
                break
        instance = extract_sub_json(f'/{inst_id}', instances)[3]
        if inst_type.upper() == 'FILE':
            data = file_data_instance(instance, data_inst_id)
        else:
            data = database_data_instance(instance, data_inst_id)
        return data
    except Exception as ex:
        message = 'Exception occurred while getting data from file or database in data Instance function'
        unify_printer(level=UNIFY_ERROR, message=message,
                          error=ex, traceback=traceback.format_exc())
        return JsonResponse(internal_server_response(message, traceback=traceback.format_exc()),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def file_data_instance(instance, data_inst_id):
    data = None
    try:
        data_frame_stmt = []
        data_frame_stmt.append("import pandas as pd")
        for data_instances in instance["dataInstances"]:
            if data_inst_id in data_instances.values():
                fun_name = data_instances["functionName"]
                args = {dataParameters["fieldName"]: dataParameters["userValue"] for dataParameters
                        in
                        data_instances["dataParameters"] if
                        dataParameters["fieldName"] != 'instanceName' and dataParameters["userValue"]}
                conn_str = fun_name + "(**" + str(args) + ")"
                data_frame_stmt.append("DataInstance = pd." + conn_str)
                break
        stmt = "\n".join(data_frame_stmt)
        exec(stmt)
        data: DataFrame = eval("DataInstance")
        return data
    except Exception as ex:
        message = 'Exception occurred while process  file data Instance'
        unify_printer(level=UNIFY_ERROR, message=message,
                          error=ex, traceback=traceback.format_exc())
        return JsonResponse(internal_server_response(message, traceback=traceback.format_exc()),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def database_data_instance(instance, data_inst_id):
    result = None
    try:
        conn_params = extract_sub_json('/connectionParameters', instance)[3]
        data_instance = extract_sub_json(f'/dataInstances/{data_inst_id}', instance)[3]
        if conn_params and data_instance:
            db_name = instance['name']
            host, port, user, password, database, instanceName = get_conn_parameters(conn_params)
            query, schema = get_query_parameters(data_instance)
            unify_printer(message=f'dn_name: {db_name}')
            unify_printer(message=f'query: {query} | schema: {schema}')
            unify_printer(
                message=f'host: {host} | port: {port} | user: {user} | password: {password} | database: {database}')
            if db_name == 'postgreSql' or db_name.upper() == 'postgres'.upper():
                result: DataFrame = process_postgres_query(db_name, host, port, user, password, query, database, schema)
            elif db_name == 'mySql':
                result: DataFrame = process_mysql_query(db_name, host, port, user, password, query, database)
            elif db_name.upper() == 'MSSQL':
                result: DataFrame = process_mssql_query(db_name, host, port, user, password, query, database)
        return result
    except Exception as ex:
        message = 'Exception occurred while process  database data Instance'
        unify_printer(level=UNIFY_ERROR, message=message,
                          error=ex, traceback=traceback.format_exc())
        return JsonResponse(internal_server_response(message, traceback=traceback.format_exc()),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


# @lru()
def source_node(flow, node_id):
    try:
        flow_json = get_flow_by_name(flow)
        query_builder = qb.Query(flow_json, flow, node_id)
        query_builder_data = query_builder.clauses()
        return query_builder_data
    except Exception as ex:
        qbuilder_prop = query_builder.qbuilder_property
        message = 'Exception occurred while process source node'
        unify_printer(level=UNIFY_ERROR, message=message,
                          error=ex, traceback=traceback.format_exc())
        return JsonResponse(internal_server_response(message, traceback=traceback.format_exc()),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


# @lru()
def join_node(flow, node_id):
    try:
        flow_json = get_flow_by_name(flow)
        query_builder = qb.Query(flow_json, flow, node_id)
        query_builder_data = query_builder.clauses()
        return query_builder_data
    except Exception as ex:
        qbuilder_prop = query_builder.qbuilder_property
        message = 'Exception occurred while process join node'
        unify_printer(level=UNIFY_ERROR, message=message,
                          error=ex, traceback=traceback.format_exc())
        return JsonResponse(internal_server_response(message, traceback=traceback.format_exc()),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


# @lru()
def union_node(flow, node_id):
    data = None
    parent_data = []
    result = pd.DataFrame()
    try:
        flow_json = get_flow_by_name(flow)
        qbuilder = qb.Query(flow_json, flow, node_id)
        result = qbuilder.clauses()
        return result
    except Exception as ex:
        qbuilder_prop = qbuilder.qbuilder_property
        message = 'Exception occurred while process union node'
        unify_printer(level=UNIFY_ERROR, message=message,
                          error=ex, traceback=traceback.format_exc())
        return JsonResponse(internal_server_response(message, traceback=traceback.format_exc()),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


def output_node(flow, node_id, flow_json):
    data = None
    parent_data = []
    result = DataFrame()
    try:
        for _, parent in flow_json.get(flow).get('nodes').get(node_id).get('data').get('parents').items():
            type = parent['type']
            parent_id = parent['id']
            if type.upper() == 'sourceNode'.upper():
                data = source_node(flow, parent_id)
                if not data.empty:
                    parent_data.append(data)
            elif type.upper() == 'unionNode'.upper():
                data = union_node(flow, parent_id)
                if not data.empty:
                    parent_data.append(data)
            elif type.upper() == 'joinNode'.upper():
                data = join_node(flow, parent_id)
                if not data.empty:
                    parent_data.append(data)
        targets = flow_json.get(flow).get('nodes').get(node_id).get('data').get('targets')
        if targets:
            args = {}
            for rec in targets:
                if rec['type'] == 'csv':
                    args = {dataparam["fieldName"]: dataparam["userValue"] for dataparam in rec.get('outputParameters')
                            if dataparam["userValue"] != None and dataparam["userValue"] != ''}
                    if args.get('index'):
                        if isinstance(args.get('index'), str):
                            import ast
                            args['index'] = ast.literal_eval(args.get('index'))
                    else:
                        args['index'] = False
                    data.to_csv(**args)
                if rec['type'] == 'excel':
                    args = {dataparam["fieldName"]: dataparam["userValue"] for dataparam in rec.get('outputParameters')
                            if dataparam["userValue"] != None and dataparam["userValue"] != ''}
                    data.to_excel(**args)

    except Exception as ex:
        raise ex


def get_join(how):
    join = ""
    if how.get('left'):
        join = join + 'L'
    if how.get('middle'):
        join = join + 'M'
    if how.get('right'):
        join = join + 'R'
    return join


# get Right and Left Parrent
def get_target_handle(flow, target_id, flow_json):
    for _, row in flow_json.get(flow).get('nodes').items():
        if row['id'].endswith('link'):
            if row['source'] == target_id:
                targetHandle = row['targetHandle']
    return targetHandle
