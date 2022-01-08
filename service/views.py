# import logging
from distutils.util import execute
import re

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view

from service.connection_types import get_connection_type_property, get_database_parameters, get_connection_types
from service.files.process_folders import process_folder_structure
from service.flows import process_flows, get_flow, get_node_counter
from service.impl.common_impl import get_restapi_params
from service.impl.database_impl import process_data_instance, meta_data_search, process_targetdata_instance
from service.impl.db_metadata import get_metadata, show_data
from service.impl.flow_instance import Data_source
from service.impl.functions.function_impl import get_functions, get_function_on_id
from service.impl.master_json import get_nodes
from service.impl.node.process_node import process_node, process_node_label, get_col_details

from service.impl.recentconnection_impl import get_recent_connections, del_recent_connections
from service.impl.single_file_impl import get_restapi_data
from service.instances import post_instance, put_instance, delete_instance, get_instances, process_custom_query
from service.util.expression_builder import process_expression, get_baron_tree, get_operators

from service.target_impl.traget_instance import create_targetDataInstances, remove_targetInstance_and_tnodeTargets
from service.target_impl.process_tconnections import get_target_types, get_subType_and_params, insert_nodeoutPut_targets, \
    get_targets
from service.target_impl.process_tnode import tnode_column_maping, send_data_to_targets

# for swagger implimentation
from service.util.unify_logger import get_logs_by_flowname, get_logs_by_request_id
from users.UserDetails import UserDetails


@csrf_exempt
@api_view(['PUT', 'DELETE'])
def process_request(request):
    # try:
    if True:
        url_path = request.path
        if not url_path.startswith('/connectionTypes'):
            pattern3 = re.compile(r'(/\w+)/.*')
            m3 = pattern3.match(url_path)
            pattern4 = re.compile(r'(/\w+)/instances/(\w+)/database(/\w+(/\w+(/\w+)?)?)?')
            m4 = pattern4.match(url_path)
        conn_obj = Data_source()
        if request.method == 'PUT':
            data = conn_obj.updateItems(request)
        elif request.method == 'DELETE':
            data = conn_obj.deleteItems(url_path)
        return data
    # except Exception as ex:
    # return JsonResponse(internal_server_response(traceback.format_exc()),
    #                     status=status.HTTP_500_INTERNAL_SERVER_ERROR)


conn_obj = Data_source()


@csrf_exempt
@api_view(['GET'])
def get_connection_type(request):
    return get_connection_types(request)


@csrf_exempt
@api_view(['GET', 'POST'])
def connection_properties(request, type):
    return get_connection_type_property(request, type)


@csrf_exempt
@api_view(['GET'])
def get_database_params(request, db_name):
    return get_database_parameters(request, db_name)


@csrf_exempt
@api_view(['GET'])
def get_fullflow(request, flow):
    UserDetails.FLOW = flow
    return get_flow(request, flow)


# pattern parameters
@api_view(['GET'])
def get_pattern_connections(request, pattern_type):
    pass
    # return get_pattern_params(request, pattern_type)


@csrf_exempt
@api_view(['POST', 'DELETE', 'GET'])
def flow(request):
    return process_flows(request)


@csrf_exempt
@api_view(['GET'])
def get_flows(request):
    return process_flows(request)


@csrf_exempt
@api_view(['GET'])
def node_counter(request, flow):
    UserDetails.FLOW = flow
    return get_node_counter(request, flow)


@csrf_exempt
@api_view(['GET'])
def get_full_flow(request, flow):
    UserDetails.FLOW = flow
    return get_flow(request, flow)


@csrf_exempt
@api_view(['GET', 'POST'])
def instances(request, flow):
    UserDetails.FLOW = flow
    if request.method == 'GET':
        return get_instances(request, flow, None)
    elif request.method == 'POST':
        return post_instance(request, flow)
    else:
        return JsonResponse(process_request(request),
                            status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['DELETE', 'GET', 'PUT'])
def instance_by_id(request, flow, instance_id):
    UserDetails.FLOW = flow
    if request.method == 'GET':
        return get_instances(request, flow, instance_id)
    elif request.method == 'PUT':
        return put_instance(request, flow, instance_id)
    elif request.method == 'DELETE':
        return delete_instance(request, flow, instance_id)
    else:
        return JsonResponse(process_request(request),
                            status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
def meta_search(request, flow, instance_id):
    UserDetails.FLOW = flow
    return meta_data_search(request, flow, instance_id)


@csrf_exempt
@api_view(['DELETE', 'GET', 'POST'])
def recentconnections(request, flow=None):
    UserDetails.FLOW = flow
    if request.method == 'GET':
        return get_recent_connections(request)
    elif request.method == 'POST':
        return get_recent_connections(request)
    elif request.method == 'DELETE':
        return del_recent_connections(request)


@csrf_exempt
@api_view(['GET', 'POST'])
def data_instances(request, flow, instance_id):
    UserDetails.FLOW = flow
    return process_data_instance(request, flow, instance_id)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def data_instance_by_id(request, flow, instance_id, data_instance_id=None):
    UserDetails.FLOW = flow
    return process_data_instance(request, flow, instance_id, data_instance_id)


@csrf_exempt
@api_view(['GET'])
def exc_data_instance(request, flow, instance_id, data_instance_id=None):
    UserDetails.FLOW = flow
    return process_data_instance(request, flow, instance_id, data_instance_id, True)


@csrf_exempt
@api_view(['POST'])
def execute_query(request, flow, instance_id):
    UserDetails.FLOW = flow
    return process_custom_query(request, flow, instance_id)


@csrf_exempt
@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def nodes(request, flow):
    UserDetails.FLOW = flow
    if request.method == 'GET':
        return get_nodes(request, flow)
    elif request.method == 'POST':
        return conn_obj.create_node(request, flow)
    elif request.method == 'DELETE':
        return conn_obj.delete_node_items(request)
    # elif request.method == 'PUT':
    #    data = conn_obj.updateItems(request,flow,flow_id)


@csrf_exempt
@api_view(['GET'])
def extract_file_data(request, flow, instance_id, data_instance_id):
    UserDetails.FLOW = flow
    return show_data(request, flow, instance_id, data_instance_id)


@csrf_exempt
@api_view(['GET', 'POST'])
def get_db_schema(request, flow, instance_id):
    UserDetails.FLOW = flow
    if request.method == 'GET':
        return get_metadata(request, flow, instance_id)
    elif request.method == 'POST':
        return get_metadata(request, flow, instance_id)


@csrf_exempt
@api_view(['GET', 'POST'])
def restapi(request):
    if request.method == 'GET':
        return get_restapi_params(request)
    if request.method == 'POST':
        return get_restapi_data(request)


# -------------------------------target section ----------------------------------------
@csrf_exempt
@api_view(['GET'])
def get_targets(request):
    return get_target_types(request)


@csrf_exempt
@api_view(['GET','POST'])
def target_subType_and_params(request, target_type):
    return get_subType_and_params(request, target_type)


@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def target_instance(request, flow, node_id):
    UserDetails.FLOW = flow
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        return create_targetDataInstances(request, flow, node_id)
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        return remove_targetInstance_and_tnodeTargets(request, flow, node_id)


@csrf_exempt
@api_view(['GET'])
def target_columns(request, flow, node_id):
    return tnode_column_maping(flow, node_id)


@csrf_exempt
@api_view(['GET'])
def run_target(request, flow, node_id):
    return send_data_to_targets(flow, node_id)


# ---------------------------------------------------------------------------------------------------
@csrf_exempt
@api_view(['GET'])
def parent_col_detail(request, flow, node_id, clause_id):
    UserDetails.FLOW = flow
    return get_col_details(flow, node_id, clause_id, True)


@csrf_exempt
@api_view(['POST'])
def target_data_instances(request, flow, instance_id):
    UserDetails.FLOW = flow
    return process_targetdata_instance(request, flow, instance_id)


@csrf_exempt
@api_view(['PUT'])
def node_label(request, flow, node_id):
    UserDetails.FLOW = flow
    return process_node_label(request, flow, node_id)


@csrf_exempt
@api_view(['POST'])
def get_folder_structure(request):
    return process_folder_structure(request)


@csrf_exempt
@api_view(['POST'])
def baron_tree(request):
    return get_baron_tree(request)


@csrf_exempt
@api_view(['GET'])
def __operators(request):
    return get_operators(request)


# ---------------------------------------------Expression-----------------------------------------------------------------

@csrf_exempt
@api_view(['POST'])
def expression_builder(request, flow, node_id, clause_id, column_id):
    UserDetails.FLOW = flow
    return process_expression(request, flow, node_id, clause_id, column_id)


@csrf_exempt
@api_view(['GET', 'POST'])
def function_list(request):
    if request.method == 'GET':
        return get_functions(request)
    else:
        return get_function_on_id(request)


# -------------------------------- LOGS -------------------------------

@csrf_exempt
@api_view(['GET'])
def get_logs_by_flow(request, flow):
    return get_logs_by_flowname(flow)


@csrf_exempt
@api_view(['GET'])
def get_logs_by_request(request, reqid):
    return get_logs_by_request_id(reqid)


@csrf_exempt
@api_view(['GET'])
def node_output(request, flow, node_id):
    UserDetails.FLOW = flow
    return process_node(request, flow, node_id)
