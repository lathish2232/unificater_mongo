import traceback
from django.http import JsonResponse
from rest_framework import status

from service.util.json_utils import  get_flow_by_name
from service.impl.node.process_node import get_parent_node_columns,get_df_from_node
from service.util.unify_response import success_response, success_response_v1, internal_server_response
from service.util.unify_logger import UNIFY_ERROR, unify_printer

#get target columns
def tnode_column_maping(flow,node_id):
    try:
        record = get_flow_by_name(flow)
        for flow_node_id in record[flow]['nodes'][node_id]['data']['parents']:
            parent_node_id=flow_node_id
        columns=get_parent_node_columns(flow,parent_node_id)
        response=JsonResponse(success_response(data=columns),status=status.HTTP_200_OK)
        return response
    except Exception as ex:
        message = 'Error occurred while gettting target column mapping'
        unify_printer(level=UNIFY_ERROR, message=message,
                          error=ex, traceback=traceback.format_exc())
        return JsonResponse(internal_server_response(message, traceback=traceback.format_exc()),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def send_data_to_targets(flow,node_id):
    try:
        path=[]
        record = get_flow_by_name(flow)
        target_list= record[flow]['nodes'][node_id]['data']['targets']
        for flow_node_id in record[flow]['nodes'][node_id]['data']['parents']:
            parent_node_id=flow_node_id
        df=get_df_from_node(record,flow,flow_node_id)
        for i, rec in enumerate(target_list):
            args,function=process_targets(record,flow, rec['id'], rec['type'])
            eval(f'df.{function}(**{args})')
            path.append(args[next(iter(args))])
        msg=f"file successfully written into this Path {path}"
        response= JsonResponse(success_response_v1(message=msg),status=status.HTTP_200_OK)
        return response
    except Exception as ex:
        message = 'Error occurred while gettting target column mapping'
        unify_printer(level=UNIFY_ERROR, message=message,
                          error=ex, traceback=traceback.format_exc())
        return JsonResponse(internal_server_response(message, traceback=traceback.format_exc()),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def process_targets(record,flow,dataInstance_id,type):
    args={}
    for rec in record[flow]['targetInstances']:
        if rec['id']==dataInstance_id:
            function =rec['functionName']
            for doc in rec['dataParameters']:
                if doc['userValue'] ==False:
                    args.update({doc['fieldName']:doc['userValue']})
                if doc['userValue']:
                    args.update({doc['fieldName']:doc['userValue']})
    return args,function
