import traceback

import pandas as pd

import service.impl.mssql.processor as mssql_processor
import service.impl.mysql.processor as mysql_processor
import service.impl.postgres.processor as psql_processor
from service.util.db_utils import get_conn_parameters, get_db_connection, get_mongod_connection
from service.util.json_utils import update_flow_by_name, insert_recent_connection, \
    extract_sub_json, update_recent_connection
from service.util.unify_logger import UNIFY_ERROR, unify_printer
from service.files.filevalidate import update_excel_data_param
from service.files.parameters import validate_file

def create_instance(record, request_body, flow_name):
    result = None
    msg = "error in connection"
    try:
        conn_params = request_body.get('connectionParameters')
        if conn_params:
            db_name = request_body['name']
            host, port, user, password, database, instanceName = get_conn_parameters(conn_params)
            conn = get_db_connection(db_name, host, port, user, password, database)
            if conn:
                id = [int(i['id'].split('_')[-1]) for i in record[flow_name]['instances']]
                inst_id = 'instanceId_' + str(1 if len(id) <= 0 else max(id) + 1)
                request_body.update({"id": inst_id, 'displayName': instanceName})
                record.get(flow_name).get('instances').append(request_body)
                result = update_flow_by_name(flow_name, record)
                flow_db = get_mongod_connection()
                insert_recent_connection(flow_db, request_body)
                msg = f"Instance '{instanceName}' created successfully!"
        else:
            msg = "Invalid instance input"
    except Exception as ex:
        unify_printer(level=UNIFY_ERROR, message='Exception occurred',
                      error=ex, traceback=traceback.format_exc())
        raise Exception(ex)
    return result, msg


def update_instance_db(record, request_body, flow_name, instance_id):
    result = False
    try:
        conn_params = request_body.get('connectionParameters')
        if conn_params:
            db_name = request_body['name']
            host, port, user, password, database, instanceName = get_conn_parameters(conn_params)
            conn = get_db_connection(db_name, host, port, user, password, database)
            if conn:
                inst_result = extract_sub_json(f'/{flow_name}/instances/{instance_id}', record)[3]
                if inst_result:
                    request_body.update({'displayName': instanceName})
                    inst_result.update(request_body)
                    result = update_flow_by_name(flow_name, record)
                    flow_db = get_mongod_connection()
                    update_recent_connection(flow_db, {'displayName': instanceName}, request_body)
                    msg = f"Instance '{instanceName}' updated successfully!"
                else:
                    msg = "Invalid instance input"
        else:
            msg = "Invalid instance input"
    except Exception as ex:
        unify_printer(level=UNIFY_ERROR, message='Exception occurred',
                      error=ex, traceback=traceback.format_exc())
        raise Exception(ex)
    return result, msg

def update_instance_file(record, request_body, flow_name, instance_id):
    try:
        if request_body['dataInstances'][0]['isActiveInFlow']:
            msg="data instance used in Flow ,Before edit please delete data instance in Designer wall "
            result=None
        else:
            for rec in request_body['dataInstances'][0]['dataParameters']:
                    if request_body['fileType'] == 'csv':
                        if rec['fieldName'] == 'filepath_or_buffer':
                            file = rec['userValue']
                    elif request_body['fileType'] == 'xlsx':
                        if rec['fieldName'] == 'io':
                            file = rec['userValue']
                        request_body['dataInstances']= update_excel_data_param(request_body,file) 
                    elif request_body['fileType'] == 'json':
                        if rec['fieldName'] == 'path_or_buf':
                            file = rec['userValue']
            request_body['displayName'] = file.split('/')[-1]
            file_validate = validate_file(file,request_body['fileType'])
            if file_validate == 'successful':
                inst_result = extract_sub_json(f'/{flow_name}/instances/{instance_id}', record)[3]
                if inst_result:
                    inst_result.update(request_body)
                    result = update_flow_by_name(flow_name, record)
                    msg = f"Instance '{request_body['displayName']}' updated successfully!"
                else:
                    msg = "Invalid instance input"
                    result=None
    except Exception as ex:
        unify_printer(level=UNIFY_ERROR, message='Exception occurred',
                      error=ex, traceback=traceback.format_exc())
        raise Exception(ex)
    return result, msg


def remove_instance(record, flow_name, instance_id):
    result = False
    try:
        inst_result = extract_sub_json(f'/{flow_name}/instances/{instance_id}', record)[3]
        if inst_result:
            instanceName = inst_result.get('displayName')
            data_instances = inst_result.get('dataInstances')
            if inst_result['type'].upper() == 'FILE':
                data_instances = inst_result.get('dataInstances')[0]
                isActive = data_instances.get('isActiveInFlow', False)
                if isActive:
                    msg = f"Instance '{instanceName}' used in Flow , Delete node belongs to this instance" \
                          f"before delete instance "
                else:
                    record.get(flow_name).get('instances').remove(inst_result)
                    result = update_flow_by_name(flow_name, record)
                    inst_result.update({'deleted': True})
                    # update_recent_connection(static_db, {'displayName': instanceName}, inst_result)
                    msg = f"Instance '{instanceName}' deleted successfully!"

            elif inst_result['type'].upper() == 'DATABASE':
                if len(data_instances) == 0:
                    record.get(flow_name).get('instances').remove(inst_result)
                    result = update_flow_by_name(flow_name, record)
                    flow_db = get_mongod_connection()
                    inst_result.update({'deleted': True})
                    update_recent_connection(flow_db, {'displayName': instanceName}, inst_result)
                    msg = f"Instance '{instanceName}' deleted successfully!"
                else:
                    msg = f"Instance '{instanceName}' not empty, It has data instance(s). Delete all data instance(s) " \
                          f"before delete instance "
        else:
            msg = f"Instance '{instance_id}' not exist!"
    except Exception as ex:
        unify_printer(level=UNIFY_ERROR, message='Exception occurred',
                      error=ex, traceback=traceback.format_exc())
        raise Exception(ex)
    return result, msg


def execute_custom_query(query, record, flow, instance_id):
    result = pd.DataFrame()
    msg = None
    try:
        instance = extract_sub_json(f'/{flow}/instances/{instance_id}', record)[3]
        conn_params = extract_sub_json('/connectionParameters', instance)[3]
        if instance and conn_params:
            db_name = instance['name']
            host, port, user, password, database, instanceName = get_conn_parameters(conn_params)
            unify_printer(
                message=f'host: {host} | port: {port} | user: {user} | password: {password} | database: {database} | db_name: {db_name} | instanceName: {instanceName}')
            if db_name.upper() == 'POSTGRESQL':
                result: pd.DataFrame = psql_processor.execute_query(db_name, host, port, user, password, query,
                                                                    database)
            elif db_name.upper() == 'MYSQL':
                result: pd.DataFrame = mysql_processor.execute_query(db_name, host, port, user, password, query,
                                                                     database)
            elif db_name.upper() == 'MSSQL':
                result: pd.DataFrame = mssql_processor.execute_query(db_name, host, port, user, password, query,
                                                                     database)
        else:
            msg = f"Invalid instance '{instance_id}'"

    except Exception as ex:
        raise ex
    return result, msg
