import traceback
import time
from django.http import JsonResponse
from rest_framework import status

from service.impl.main_uniflow import updateMasterJsonItems, deleteMasterJsonItems
from service.impl.node.process_node import insert_nl, delete_node, clear_node_functions
from service.util.json_utils import extract_sub_json, get_flow_by_name, update_flow_by_name
from service.util.unify_logger import UNIFY_ERROR, unify_printer
from service.util.unify_response import success_response, not_accepted_response, no_content_response, \
    success_delete_response, internal_server_response
from service.util.user_db_conn_validation import instance_db_validation

conn_validation = instance_db_validation()


class Data_source():
    def __init__(self):
        pass

    def deleteItems(self, urlpath):
        collection = urlpath.split('/')[1]
        record = get_flow_by_name(collection)
        keys = extract_sub_json(urlpath, record)[1]
        deleteMasterJsonItems(record, keys)
        result = update_flow_by_name(collection, record)
        return result

    def updateItems(self, request):
        try:
            collection = request.get_full_path().split('/')[1]
            urlpath = request.get_full_path().split('/?')[-1]
            values = request.data
            record = get_flow_by_name(collection)
            keys = extract_sub_json(urlpath, record)[1]
            updateMasterJsonItems(record, keys, values)
            update_flow_by_name(collection, record)
            if keys[-1] == 'query' and keys[1] == 'nodes':
                node_id = keys[2]
                flow_name = keys[0]
                links = [x for x in record[flow_name]['nodes'].keys() if x.endswith('-link')]
                # clear_node_functions(record, flow_name, links, node_id, True)
            return JsonResponse(success_response(data="updated successfylly"), status=status.HTTP_200_OK)
        except Exception as ex:
            message = 'Exception occurred while update'
            unify_printer(level=UNIFY_ERROR, message=message,
                          error=ex, traceback=traceback.format_exc())
            return JsonResponse(internal_server_response(message, traceback=traceback.format_exc()),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create_node(self, request,flow):
        try:
            request_body = request.data
            record = get_flow_by_name(flow)
            if record:
                if isinstance(request_body, dict):
                    if request_body:
                        insert_nl(request_body, flow, record)
                        data=update_flow_by_name(flow, record)
                    if data:
                        return JsonResponse(success_response(data=data), status=status.HTTP_200_OK)
                    else:
                        return JsonResponse(not_accepted_response(message=f" is not a valid request"),
                        status=status.HTTP_406_NOT_ACCEPTABLE)
                else:
                    return JsonResponse(
                        not_accepted_response(message=f"{type(request_body).__name__} is not a valid request"),
                    status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                message="while fetching flow data have issue"
                return JsonResponse(internal_server_response(message, traceback.format_exc()),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as ex:
            message = 'Error occurred while create instance'
            unify_printer(level=UNIFY_ERROR, message=message, error=ex, traceback=traceback.format_exc())
            return JsonResponse(internal_server_response(message, traceback.format_exc()),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete_node_items(self, request):
        if True:
            # try:
            del_key = request.data
            url = request.get_full_path()
            collection = url.split('/')[1]
            record = get_flow_by_name(collection)
            ufid = record[collection]['UFID']
            delete_node(request.data, collection, record)
            update_flow_by_name(collection, record)
            return JsonResponse(success_delete_response(message=f"{del_key} has been deleted successfully"),
                                status=status.HTTP_200_OK)
