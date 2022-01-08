import time
import traceback

from django.http import JsonResponse
from rest_framework import status

from service.util.db_utils import  get_flow_by_name
from service.util.unify_logger import unify_printer, UNIFY_ERROR
from service.util.unify_response import success_response, internal_server_response, no_content_response,success_response_v1  # write_audit

def get_nodes(request, flow):
    try:
        start = time.time()
        unify_printer(message='Get flow')
        data = get_flow_by_name(flow)
        if data:
            record=data[flow]['nodes']
            response = success_response_v1(data=record)
        else:
            response = no_content_response()
        json_response = JsonResponse(response, status=status.HTTP_200_OK)
    except Exception as ex:
        message = 'Exception occurred while getting flow'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # write_audit(request, response, start, time.time())
    return json_response


def dataInstance(master_json, instance_id, data_instance_id):
    Data_frame_stmt = []
    Data_frame_stmt.append("import pandas as pd")
    instances = master_json.get('file_flow').get("instances")
    for instance in instances:
        if instance_id in instance.values():
            for data_instance_dict in instance["dataInstances"]:
                if data_instance_id in data_instance_dict.values():
                    fun_name = data_instance_dict["functionName"]
                    args = {dataParameters_dict["fieldName"]: dataParameters_dict["userValue"] for dataParameters_dict
                            in data_instance_dict["dataParameters"] if
                            dataParameters_dict["fieldName"] != 'instanceName' and dataParameters_dict["userValue"]}
                    conn_str = fun_name + "(**" + str(args) + ")"
                    Data_frame_stmt.append("DataInstance = pd." + conn_str)
                    break
            break
    stmt = "\n".join(Data_frame_stmt)
    exec(stmt)
    return eval("DataInstance")
