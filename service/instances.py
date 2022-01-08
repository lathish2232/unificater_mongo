import os
import glob
import json
import traceback

import sqlvalidator
from django.http import JsonResponse
from rest_framework import status

from service.databases.impl.process_instance import create_instance, update_instance_db, remove_instance, \
    execute_custom_query, update_instance_file
from service.files.parameters import validate_file
from service.util.http_constances import invalid_msg
from service.util.json_utils import get_flow_by_name, extract_sub_json, insert_json_items, update_flow_by_name
from service.util.unify_logger import unify_printer, UNIFY_ERROR
from service.util.unify_response import internal_server_response, validation_error_response, success_response, \
    no_content_response, not_accepted_response, service_not_available_response, success_delete_response
from service.util.validater import do_instance_validation
from service.files.filevalidate import Filevalidate, update_excel_data_param


def post_instance(request, flow):
    try:
        request_body = request.data
        record: dict = get_flow_by_name(flow)
        if request_body["type"] == "database":
            result, msg = create_instance(record, request_body, flow)
            if result:
                response = success_response(message=msg, data=result)
                return JsonResponse(response, status=status.HTTP_201_CREATED)
            else:
                response = validation_error_response(msg)
        else:
            if request_body["type"].upper() == 'FILE':
                for rec in request_body['dataInstances'][0]['dataParameters']:
                    if request_body['fileType'] == 'csv':
                        if rec['fieldName'] == 'filepath_or_buffer':
                            file = rec['userValue']
                        request_body['displayName'] = os.path.basename(file)
                    elif request_body['fileType'] == 'xlsx':
                        if rec['fieldName'] == 'io':
                            file = rec['userValue']
                            request_body['dataInstances'] = update_excel_data_param(request_body, file)
                        request_body['displayName'] = os.path.basename(file)
                        break
                    elif request_body['fileType'] == 'json':
                        if rec['fieldName'] == 'path_or_buf':
                            file = rec['userValue']
                        request_body['displayName'] = os.path.basename(file)
                file_validate = validate_file(file, request_body['fileType'])
            elif request_body["type"].upper() == "PATTERN":
                for rec in request_body['dataInstances']:
                    for row in rec['dataParameters']:
                        if row['fieldName'] == 'filepath_or_buffer':
                            files = glob.glob(row['userValue'])
                if files:
                    for file in files:
                        file_validate = validate_file(file)

            if file_validate == 'successful':
                id = [int(i['id'].split('_')[-1]) for i in record[flow]['instances']]
                inst_id = 'instanceId_' + str(1 if len(id) <= 0 else max(id) + 1)
                request_body.update({"id": inst_id})
                url = request.get_full_path()
                _, keys, _, json = extract_sub_json(url, record)
                insert_json_items(record, keys, 0, request_body)
                data = update_flow_by_name(flow, record)
                response = success_response(data=data)
            else:
                response = validation_error_response(file_validate)
        # else:
        #     response = validation_error_response(inst_validation)
        json_response = JsonResponse(response, status=status.HTTP_200_OK)
    except Exception as ex:
        message = 'Exception occurred while POST instance'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return json_response


def put_instance(request, flow_name, instance_id):
    try:
        request_body = request.data
        # inst_validation = do_instance_validation(request_body)
        record: dict = get_flow_by_name(flow_name)
        if request_body["type"] == "database":
            result, msg = update_instance_db(record, request_body, flow_name, instance_id)
            if result:
                response = success_response(message=msg, data=result)
            else:
                response = validation_error_response(msg)
        elif request_body["type"] == "file":
            result, msg = update_instance_file(record, request_body, flow_name, instance_id)
            if result:
                response = success_response(message=msg, data=result)
            else:
                response = validation_error_response(msg)
            json_response = JsonResponse(response, status=status.HTTP_200_OK)
            return json_response
        else:
            response = not_accepted_response(f"Instance type {request_body['type']} is not supported.")
        json_response = JsonResponse(response, status=status.HTTP_200_OK)
    except Exception as ex:
        message = 'Exception occurred while PUT instance'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return json_response


def delete_instance(request, flow_name, instance_id):
    try:
        record: dict = get_flow_by_name(flow_name)
        result, msg = remove_instance(record, flow_name, instance_id)
        if result:
            response = success_delete_response(message=msg, data=result)
        else:
            response = validation_error_response(msg)
        json_response = JsonResponse(response, status=status.HTTP_200_OK)
    except Exception as ex:
        message = 'Exception occurred while DELETE instance'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return json_response


def get_instances(request, flow_name, instance_id):
    try:
        data = get_flow_by_name(flow_name)
        if instance_id:
            data = extract_sub_json(f'/{flow_name}/instances/{instance_id}', data)[3]
            response = success_response(data=data)
        elif data:
            data = extract_sub_json(f'/{flow_name}/instances', data)[3]
            if data:
                response = success_response(data=data)
            else:
                response = no_content_response(message='Instance not available on this flow')
        else:
            response = no_content_response(message='Flow not available.')
        json_response = JsonResponse(response, status=status.HTTP_200_OK)
    except Exception as ex:
        message = 'Exception occurred while GET instance'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return json_response


def process_custom_query(request, flow, instance_id):
    try:
        body = request.data
        if body:
            query = body['query']
            sql_query = sqlvalidator.parse(query)
            if sql_query.is_valid():
                record: dict = get_flow_by_name(flow)
                result, msg = execute_custom_query(query, record, flow, instance_id)
                if msg:
                    response = validation_error_response(msg)
                else:
                    if not result.empty:
                        result = result.to_json(orient='records', date_format='iso')
                        result = json.loads(result)
                        response = success_response(data=result)
                    else:
                        response = no_content_response()
        else:
            response = validation_error_response(invalid_msg)
        json_response = JsonResponse(response, status=status.HTTP_200_OK)
    except Exception as ex:
        message = 'Exception occurred while GET instance'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return json_response
