import os 
import json
import traceback
from django.http.response import JsonResponse

from rest_framework import status

from service.util.json_utils import get_flow_by_name, update_flow_by_name, extract_sub_json, insert_json_items
from service.util.unify_response import internal_server_response, validation_error_response, success_response, \
    no_content_response, not_accepted_response, service_not_available_response, success_delete_response
from service.util.unify_logger import unify_printer, UNIFY_ERROR
from service.impl.node.process_node import get_parent_node_columns


# Add targets in to flow 
def create_targetDataInstances(request, flow, node_id):
    request_body = request.data
    record = get_flow_by_name(flow)
    target_instance = record[flow]['targetInstances']
    if target_instance:
        id = [int(i['id'].split('_')[-1]) for i in record[flow]['targetInstances']]
        dataInst_id = 'dataInstanceId_' + str(1 if len(id) <= 0 else max(id) + 1)
    else:
        dataInst_id = 'dataInstanceId_1'
    request_body["id"] = dataInst_id
    target_instance.append(request_body)
    request_body['nodeId'] = node_id
    if request_body['type'] == 'file':
        response=create_file_instance(request_body,record,flow, node_id,dataInst_id)
    elif request_body['type']=="database":
        pass
    return response


def insert_target_to_taraget_node(record, flow, nodeId, dataInstanceId, path,sheetname, tType):
    node_data = record[flow]['nodes'][nodeId]['data']
    file_name=os.path.basename(path)
    for flow_node_id in record[flow]['nodes'][nodeId]['data']['parents']:
        parent_node_id = flow_node_id
    column = get_parent_node_columns(flow, parent_node_id, record)
    doc={'id': dataInstanceId, 'name': file_name,'displayName':f'{file_name} {sheetname}', 'type': tType, 'columnMapping': column}
    if node_data.get('targets'):
        node_data['targets'].append(doc)
    else:
        targets = [doc]
        node_data.update({'targets': targets})
    update_flow_by_name(flow, record)
    for rec in node_data['targets']:
        del rec['columnMapping']
    return node_data['targets']


# remove target data instances from flow 
def remove_targetInstance_and_tnodeTargets(request, flow, node_id):
    try:
        id = request.data['id']
        record = get_flow_by_name(flow)
        target_instance = record[flow]['targetInstances']
        for index, rec in enumerate(target_instance):
            if rec['id'] == id:
                name = rec['displayName']
                target_instance.pop(index)
                remove_trget_in_tnode(record, flow, node_id, id)
                data = update_flow_by_name(flow, record)
                msg = f'{name} target deleted Successflly'
                json_response = response = JsonResponse(success_delete_response(message=msg, data=data),
                                                        status=status.HTTP_200_OK)
            else:
                msg = f' id not Exists in targets'
                json_response = response = JsonResponse(not_accepted_response(message=msg),
                                                status=status.HTTP_200_OK)
    except Exception as ex:
        message = 'Exception occurred while DELETE instance'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return json_response


# remove target reference  in target node
def remove_trget_in_tnode(record, flow, nodeId, id):
    node_targets = record[flow]['nodes'][nodeId]['data']['targets']
    for index, rec in enumerate(node_targets):
        if rec['id'] == id:
            node_targets.pop(index)


def create_file_instance(payload,record,flow, node_id,dataInst_id):
    sheetname=''
    for rec in payload['dataParameters']:
            if rec['id'] == 'fieldId_1':
                file = rec['userValue']
            if payload['fileType']=='xlsx':
                if rec['id'] == 'fieldId_2':
                    sheetname = f"({rec['userValue']})"
    if not file:
        msg = 'File path is empty,please provide valid path'
        response = JsonResponse(validation_error_response(msg), status=status.HTTP_406_NOT_ACCEPTABLE)
    elif file:
        payload['displayName'] = file.split('/')[-1]
        if payload["isFileExists"]:
            pass
        else:
            targets = insert_target_to_taraget_node(record, flow, node_id, dataInst_id, file,sheetname,
                                                    payload['type'])
            response = JsonResponse(success_response(data=targets), status=status.HTTP_200_OK)
    return response
