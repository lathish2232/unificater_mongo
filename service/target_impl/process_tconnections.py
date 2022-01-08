
import os
import time
import traceback
from uuid import uuid4

from django.http import JsonResponse
from rest_framework import status

from service.util.db_utils import get_data_from_targetTypes
from service.util.json_utils import extract_sub_json, get_flow_by_name, update_flow_by_name
from service.util.node_utils import  output_node
from service.util.unify_logger import UNIFY_ERROR, unify_printer
from service.util.unify_response import success_response, success_create_response, validation_error_response, no_content_response, internal_server_response  # write_audit
from service.util.unify_uris import TARGET_TYPE_ID
from service.target_impl.target_conn import get_databaseTypes,get_file_params,get_db_params
from service.target_impl.target_validation import get_target_xlsheets

def get_target_types(request):
    try:
        url = request.get_full_path()
        output_types = get_data_from_targetTypes('targetTypes', url)
        if output_types:
            for row in output_types:
                del row['connections']
        json_response= JsonResponse(success_response(data=output_types), status=status.HTTP_200_OK)
    except Exception as ex:
        message = 'Error occurred while Getting target types'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return json_response


def get_subType_and_params(request, target_type):
    try:
        if request.method=='GET':
            if target_type == "database":
                record=get_databaseTypes()
                return JsonResponse(success_response(data=record), status=status.HTTP_200_OK)
        elif request.method == 'POST' and target_type == "database":
            record=get_db_params(request,target_type)
            response= JsonResponse(success_response(data=record), status=status.HTTP_200_OK)
        elif request.method == 'POST' and target_type == "file":
            filePath = request.data.get('filePath')
            fileType = request.data.get('fileType')
            if filePath:
                record=get_target_xlsheets(filePath)
                response= JsonResponse(success_response(data=record), status=status.HTTP_200_OK)
            elif fileType:
                record=get_file_params(target_type,fileType)
                response= JsonResponse(success_response(data=record), status=status.HTTP_200_OK)
        return response
    except Exception as ex:
        msg='Error occurred while geting target parameters'
        unify_printer(level=UNIFY_ERROR, message=msg, error=ex,
                      traceback=traceback.format_exc())
        response = internal_server_response(traceback.format_exc())
        json_response = JsonResponse(
            response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return json_response

def insert_nodeoutPut_targets(request, flow, node_id):
    url = f'/{flow}/nodes/{node_id}'
    request_body = request.data
    flow_records = get_flow_by_name(flow)
    params = extract_sub_json(url, flow_records)[3]
    targets = params['data'].get('targets')
    if request_body:
        if targets:
            for rec in request_body.get('targets'):
                for row in rec['outputParameters']:
                    if row['id'] == 'fieldId_1':
                        rec['displayName'] = row['userValue'].split('/')[-1]
                rec.update({"id": str(uuid4())})
                targets.append(rec)
        else:
            for rec in request_body.get('targets'):
                rec.update({"id": str(uuid4())})
            params['data'].update(request_body)
        result = update_flow_by_name(flow, flow_records)
        return JsonResponse(success_create_response(message="records updated successfully", data=result),
                            status=status.HTTP_200_OK)
    else:
        return JsonResponse(validation_error_response(message='invalid request,payload should not be empty '),
                            status=status.HTTP_400_BAD_REQUEST)


def get_targets(request, flow, node_id):
    url = f'/{flow}/nodes/{node_id}/data/targets'
    flow_records = get_flow_by_name(flow)
    params = extract_sub_json(url, flow_records)[3]
    if params:
        for rec in params:
            del rec['outputParameters']
            del rec['functionName']
        return JsonResponse(success_response(data=params), status=status.HTTP_200_OK)
    else:
        return JsonResponse(no_content_response(message='id Not Exists'), status=status.HTTP_200_OK)

def update_targets(request, flow, node_id):
    pass


#---current version bellow functions not using---commented By :-Lathish

def run_output(request, flow, node_id):
    flow_json = get_flow_by_name(flow)
    url = f'/{flow}/nodes/{node_id}/data/targets'
    try:
        targets = extract_sub_json(url, flow_json)[3]
        file_paths = []
        for rec in targets:
            for row in rec['outputParameters']:
                if row['fieldName'] == 'path_or_buf':
                    path = row['userValue']
                    file_paths.append(path)
        output_node(flow, node_id, flow_json)
        data = {'status': 'File Downloaded', 'filePath': file_paths}
        response = success_response(data=data)
        json_response = JsonResponse(response, status=status.HTTP_200_OK)
    except Exception as ex:
        unify_printer(level=UNIFY_ERROR, message='Error occurred while get output of the node', error=ex,
                      traceback=traceback.format_exc())
        response = internal_server_response(traceback.format_exc())
        json_response = JsonResponse(
            response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return json_response
