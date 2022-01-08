import glob
import json
import traceback

import pandas as pd
from django.http import JsonResponse
from rest_framework import status
from sqlalchemy import create_engine

from service.impl.refpkg.cache import clear_all_cached_functions, clearable_lru_cache
from service.util.db_utils import connection_str
from service.util.json_utils import get_flow_by_name
from service.util.unify_logger import unify_printer, UNIFY_ERROR
from service.util.unify_response import success_response, unauthorized, no_content_response, internal_server_response, \
    validation_error_response


def getCollectionData(urlpath):
    collection = urlpath.split('/')[1]
    record = get_flow_by_name(collection)
    return record


def get_metadata(request, flow, instance_id):
    json_response = None
    try:
        master_json = get_flow_by_name(flow)
        instances = master_json.get(flow).get('instances')
        connection_string = connection_str(instance_id, instances)
        if connection_string:
            info = request.data
            meta_data = []
            id = 1
            connection = None
            for instance in instances:
                if instance['type'] == 'database':
                    unify_printer(message=f"instance['name']: {instance['name']}")
                    if instance.get('id') == instance_id:
                        #try:
                        if True:
                            if instance['name'] == 'postgreSql':
                                connection = create_engine(connection_string)
                                if request.method == 'POST':
                                    if info:
                                        metaType = info.get('info', '').split('>')[-1]
                                        schema = info.get('info', '').split('>')[0]
                                        if metaType == "tables":
                                            sql = f"""
                                                select distinct table_catalog as "dbName", table_schema as "tableSchema",TABLE_NAME as "tableName" from INFORMATION_SCHEMA.columns
                                                WHERE table_schema = '{schema}' ORDER BY table_name;"""
                                        elif metaType == "columns":
                                            tName = info.get('info', '').split('>')[1]
                                            sql = f"""
                                                    select table_catalog as "dbName" ,table_schema as "tableSchema",table_name as "tableName" ,COLUMN_NAME as"columnName", data_type as"dataType" from INFORMATION_SCHEMA.columns
                                                    WHERE table_schema = '{schema}' and table_name='{tName}' ORDER BY ORDINAL_POSITION;"""
                                        idtype = metaType[:-1]
                                    else:
                                        json_response = JsonResponse(no_content_response(),
                                                                     status=status.HTTP_204_NO_CONTENT)
                                elif request.method == 'GET':
                                    sql = """select catalog_name as "dbName",schema_name as "schemaName" from
                                                information_schema.schemata;"""
                                    idtype = 'schema'
                            elif instance['name'] == 'mySql':
                                connection = create_engine(connection_string)
                                if request.method == 'POST':
                                    if info:
                                        metaType = info.get('info', '').split('>')[-1]
                                        table = info.get('info', '').split('>')[1]
                                        schema = info.get('info', '').split('>')[0]
                                        if metaType == "tables":
                                            sql = f"""
                                                    Select Distinct table_schema as schemaName,table_name as tableName 
                                                    from INFORMATION_SCHEMA.columns where table_schema ='{schema}' order By table_name  ;"""
                                        elif metaType == "columns":
                                            sql = f"""Select Distinct table_schema as schemaName,table_name as tableName,column_name as columnName ,
                                                        data_Type as dataType from INFORMATION_SCHEMA.columns where table_schema ='{schema}' 
                                                        and table_name='{table}' order by table_name"""
                                        idtype = metaType[:-1]
                                    else:
                                        json_response = JsonResponse(no_content_response(),
                                                                     status=status.HTTP_204_NO_CONTENT)
                                elif request.method == 'GET':
                                    sql = "select distinct table_schema as schemaName,'false' as isDatabase from information_schema.tables"
                                    idtype = 'schema'
                            elif instance['name'].upper() == 'MSSQL':
                                connection = create_engine(connection_string)
                                if request.method == 'POST':
                                    if info:
                                        metaType = info.get('info', '').split('>')[-1]
                                        table = info.get('info', '').split('>')[1]
                                        schema = info.get('info', '').split('>')[0]
                                        if metaType == "tables":
                                            sql = f"""
                                                    Select Distinct table_schema as schemaName,table_name as tableName 
                                                    from INFORMATION_SCHEMA.columns where table_schema ='{schema}' order By table_name  ;"""
                                        elif metaType == "columns":
                                            sql = f"""Select Distinct table_schema as schemaName,table_name as tableName,column_name as columnName ,
                                                        data_Type as dataType from INFORMATION_SCHEMA.columns where table_schema ='{schema}' 
                                                        and table_name='{table}' order by table_name"""
                                        idtype = metaType[:-1]
                                    else:
                                        json_response = JsonResponse(no_content_response(),
                                                                     status=status.HTTP_204_NO_CONTENT)
                                elif request.method == 'GET':
                                    sql = "select distinct table_schema as schemaName,'false' as isDatabase from information_schema.tables"
                                    idtype = 'schema'
                            result = [list(i) for i in connection.execute(sql)]
                            columnnames = [i for i in connection.execute(sql).keys()]
                            for row in result:
                                if row[1] == 'false':
                                    row[1] = False
                                meta_data.append(dict(zip(columnnames, row)))
                            for item in meta_data:
                                item.update({'id': idtype + 'Id_' + str(id)})
                                id = id + 1
                            if len(meta_data) == 0:
                                json_response = JsonResponse(success_response(data=meta_data),
                                                             status=status.HTTP_200_OK)
                            else:
                                json_response = JsonResponse(success_response(data=meta_data),
                                                             status=status.HTTP_200_OK)
                        # except Exception as error:
                        #     json_response = JsonResponse(unauthorized(error=str(error).rstrip('\n')),
                        #                                  status=status.HTTP_401_UNAUTHORIZED)
                        # finally:
                        #     if connection:
                        #         connection.dispose()
        else:
            json_response = JsonResponse(validation_error_response(message='Instance or connection not available'),
                                         status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        message = 'Exception occurred while get meta data'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        json_response = JsonResponse(internal_server_response(message, traceback.format_exc()),
                                     status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return json_response


def show_data(request, flow, instance_id, data_instance_id):
    try:
        df_json = {}
        # record = flowdb[flow].find_one({}, {'_id': 0})
        start = None
        end = None
        queryRange = request.query_params.get('range', None)
        if queryRange:
            range = queryRange.split('-')
            start = int(range[0])
            end = int(range[1])
            #if not start:
                # data_instance.clear_cache()
                #clear_all_cached_functions()
        df = data_instance(instance_id, data_instance_id, flow)
        df_json['columns'] = list(df.columns)
        if start:
            df_json['counts'] = None
        else:
            df_json['counts'] = {'columns': df.shape[1], 'rows': df.shape[0]}
        df_json['rows'] = json.loads(df.loc[start:end, :].to_json(orient="records", date_format='iso'))
        return JsonResponse(success_response(data=df_json), status=status.HTTP_200_OK)
    except Exception as ex:
        message = 'Exception occurred while extract data'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        return JsonResponse(internal_server_response(message, traceback.format_exc()), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#@clearable_lru_cache()
def data_instance(instance_id, datainstance_id, flow):
    try:
        master_json = get_flow_by_name(flow)
        instances = master_json.get(flow).get('instances')
        for instance in instances:
            if instance.get('id') == instance_id:
                if instance['type'] == 'database':
                    connection_string = connection_str(instance_id, instances)
                    for item in instance.get('dataInstances'):
                        if item.get('id') == datainstance_id:
                            table = item.get('table')
                            query = item.get('query')
                            dbschema = item.get('schema')
                        if table:
                            df = pd.read_sql_table(table, create_engine(connection_string), schema=dbschema)
                        else:
                            df = pd.read_sql(query, create_engine(connection_string))
                elif instance['type'] == 'file':
                    args = {}
                    for item in instance.get('dataInstances'):
                        if item.get('id') == datainstance_id:
                            args = {dataparam["fieldName"]: dataparam["userValue"] for dataparam in
                                    item.get('dataParameters') if
                                    dataparam["userValue"] != None and dataparam["userValue"] != ''}
                            # args ={dataparam["fieldName"]: dataparam["userValue"] for dataparam in item.get('dataParameters') if dataparam["userValue"] != dataparam['parameterDefaultValue']}
                    for key,value in args.items():
                        if isinstance(value,str) and value.isdigit():
                            args.update({key:int(value)})
                    if instance['fileType'] == 'csv':
                        df = pd.read_csv(**args)
                        # df = pd.read_csv(**args)
                    elif instance['fileType'] == 'xlsx':
                        df = pd.read_excel(**args, engine='openpyxl')
                    elif instance['fileType'] == 'json':
                        df = pd.read_json(**args)
                elif instance['type'] == "pattern" and instance['name'] == 'csv':
                    for item in instance.get('dataInstances'):
                        if item.get('id') == datainstance_id:
                            for rec in item['dataParameters']:
                                if rec['fieldName'] == 'filepath_or_buffer':
                                    files = glob.glob(rec['userValue'])
                    if files:
                        df = pd.concat(map(pd.read_csv, files))
        return df
    except Exception as ex:
        return ex
    finally:
        pass
