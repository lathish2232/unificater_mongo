import time
import time
import traceback
from datetime import datetime
from uuid import uuid4

from django.http import JsonResponse
from rest_framework import status

from service.util.db_utils import get_mongod_connection, FLOW_DB
from service.util.json_utils import get_flow_by_name
from service.util.unify_logger import UNIFY_ERROR, unify_printer
from service.util.unify_response import success_create_response, duplicate_content_response, internal_server_response \
    , success_response, success_delete_response, not_accepted_response, no_content_response, \
    validation_error_response
from users.UserDetails import UserDetails


def process_flows(request):
    if request.method == 'POST':
        return create_flow(request)
    elif request.method == 'GET':
        return get_all_flows(request)
    elif request.method == 'DELETE':
        return delete_flow(request)


def create_flow(request):
    try:
        flow_name = request.data.get('name', None)
        flow_db = get_mongod_connection(FLOW_DB)
        flow_exist = flow_db['flows'].find_one({'$and': [{"flowName": flow_name}, {"userId": UserDetails.LOGGED_IN_USER_ID}]})
        if flow_name:
            if not flow_exist:
                flow_templete = {
                    "UFID": None,
                    "nodeCounter": 0,
                    "instances": [],
                    "nodes": {},
                    "targetInstances": []
                }
                int(flow_templete['nodeCounter'])
                flow_templete['UFID'] = str(uuid4())
                flow_doc = {
                    "UFID": str(uuid4()),
                    "flowName": flow_name,
                    "userId": UserDetails.LOGGED_IN_USER_ID,
                    flow_name: flow_templete,
                    "createdOn": datetime.now(),
                    "createdBy": UserDetails.LOGGED_IN_USER_NAME,
                    "modifiedOn": None,
                    "modifiedBy": None
                }
                flow_db['flows'].insert_one(flow_doc)
                response = success_create_response(f'Flow {flow_name} created successfully.', data=flow_doc[flow_name])
                meta_doc = {"flowName": flow_name, "createdBy": UserDetails.LOGGED_IN_USER_ID,
                            "createdOn": datetime.now(), "modifiedOn": None, "modifiedBy": None}
                json_response = JsonResponse(response, status=status.HTTP_201_CREATED)
            else:
                response = duplicate_content_response('Flow already exist.')
                json_response = JsonResponse(response, status=status.HTTP_409_CONFLICT)
        else:
            response = not_accepted_response('empty values not accptable. please provid valid flow name')
            json_response = JsonResponse(response, status=status.HTTP_406_NOT_ACCEPTABLE)
    except Exception as ex:
        message = 'Exception occurred while create flow'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return json_response


def get_all_flows(request):
    try:
        record = get_all_flow_name()
        if record:
            response = success_response(data=record)
        else:
            response = no_content_response(message='No Flow available.')
        json_response = JsonResponse(response, status=status.HTTP_200_OK)
    except Exception as ex:
        message = 'Exception occurred while get all flow'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return json_response


def delete_flow(request):
    try:
        start = time.time()
        flow_name = request.data.get('name', None)
        if flow_name:
            flow_db = get_mongod_connection(FLOW_DB)
            result = flow_db.flows.find_one_and_delete({'flowName': flow_name,"userId": UserDetails.LOGGED_IN_USER_ID})
            if result:
                response = success_delete_response(message=f'Flow \'{flow_name}\' has been deleted successfully')
            else:
                response = not_accepted_response(message=f'Flow \'{flow_name}\' not exist')
        else:
            response = validation_error_response(message="name is required")
        json_response = JsonResponse(response, status=status.HTTP_200_OK)
    except Exception as ex:
        message = 'Exception occurred while get delete flow'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return json_response


def get_all_flow_name():
    flows = None
    try:
        flow_db = get_mongod_connection(FLOW_DB)
        record = flow_db.flows.find({"userId": UserDetails.LOGGED_IN_USER_ID},
                                    {'flowName': 1, 'createdOn': 1, 'createdBy': 1, 'modifiedOn': 1, 'modifiedBy': 1,
                                     '_id': 0})
        flows = [row for row in record]
    except Exception as ex:
        raise Exception(ex)
    return flows


def get_flow(request, flow):
    try:
        data = get_flow_by_name(flow)
        if data:
            response = success_response(data=data)
        else:
            response = no_content_response(message=f"flow '{flow}' not exist")
        return JsonResponse(response, status=status.HTTP_200_OK)
    except Exception as ex:
        message = 'Exception occurred while get full flow'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
    return JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_node_counter(request, flow):
    flow_data = get_flow_by_name(flow)
    response = success_response(data={'nodeCounter': flow_data[flow]['nodeCounter']})
    return JsonResponse(response, status=status.HTTP_200_OK)
