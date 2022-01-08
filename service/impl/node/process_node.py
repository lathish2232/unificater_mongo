import json
import time
import traceback

from django.http import JsonResponse
from pandas import DataFrame
from rest_framework import status

from service.impl.query_builder import Query
from service.util.http_constances import invalid_input
from service.util.json_utils import extract_sub_json, get_flow_by_name, get_node_type, update_flow_by_name
from service.util.node_utils import source_node, join_node, union_node
# get_cols, join_node_col_details, join_col_details #,source_column_details
from service.util.unify_logger import UNIFY_ERROR, unify_printer
from service.util.unify_response import success_response, no_content_response, internal_server_response, \
    validation_error_response, not_accepted_response  # write_audit


def insert_node(node_json, flow_name, master_json):
    try:
        master_json[flow_name]['nodeCounter'] = [key.split('__')[-1] for key in node_json.keys()][0]
        master_json[flow_name]['nodes'].update(node_json)
    except Exception as ex:
        message = 'Exception occurred while insert node'
        unify_printer(level=UNIFY_ERROR, message=message,
                          error=ex, traceback=traceback.format_exc())
        return JsonResponse(internal_server_response(message, traceback=traceback.format_exc()),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def insert_nl(nl_json, flow_name, master_json):
    try:
        # it will insert nodes and links
        nodes = {}
        links = {}
        for key in nl_json.keys():
            if key.endswith('-link'):
                links[key] = nl_json[key]
                for key in links.keys():
                    create_link(key, links[key], flow_name, master_json)
            else:
                nodes[key] = nl_json[key]
                insert_node(nodes, flow_name, master_json)
    except Exception as ex:
        message = 'Exception occurred while insert nodes and links'
        unify_printer(level=UNIFY_ERROR, message=message,
                          error=ex, traceback=traceback.format_exc())
        return JsonResponse(internal_server_response(message, traceback=traceback.format_exc()),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def create_link(key, val, flow_name, master_json):
    try:
        # Create Link
        master_json[flow_name]['nodes'][key] = val
        # Get the information of the source and target of the link
        source_id = master_json[flow_name]['nodes'][key]['source']
        target_id = master_json[flow_name]['nodes'][key]['target']
        # Get type
        source_type = master_json[flow_name]['nodes'][source_id]['data']['type']
        target_type = master_json[flow_name]['nodes'][target_id]['data']['type']
        # Get name
        source_name = master_json[flow_name]['nodes'][source_id]['data']['label']
        target_name = master_json[flow_name]['nodes'][target_id]['data']['label']
        # Update children information at source
        master_json[flow_name]['nodes'][source_id]['data']['children'][target_id] = {'id': target_id}
        master_json[flow_name]['nodes'][source_id]['data']['children'][target_id]['type'] = target_type
        master_json[flow_name]['nodes'][source_id]['data']['children'][target_id]['name'] = target_name
        # Update parents information at target
        master_json[flow_name]['nodes'][target_id]['data']['parents'][source_id] = {'id': source_id}
        master_json[flow_name]['nodes'][target_id]['data']['parents'][source_id]['type'] = source_type
        master_json[flow_name]['nodes'][target_id]['data']['parents'][source_id]['name'] = source_name
    except Exception as ex:
        message = 'Exception occurred while insert create link'
        unify_printer(level=UNIFY_ERROR, message=message,
                          error=ex, traceback=traceback.format_exc())
        return JsonResponse(internal_server_response(message, traceback=traceback.format_exc()),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def find_descendants(master_json, flow_name, links, node_id, descendants):
    try:
        for i in links:
            if master_json[flow_name]['nodes'][i]['source'] == node_id:
                descendants.append(master_json[flow_name]['nodes'][i].get('target'))
                find_descendants(master_json, flow_name, links, master_json[flow_name]['nodes'][i].get('target'),
                                descendants)
    except Exception as ex:
        message = 'Exception occurred while find descendants in process node'
        unify_printer(level=UNIFY_ERROR, message=message,
                          error=ex, traceback=traceback.format_exc())
        return JsonResponse(internal_server_response(message, traceback=traceback.format_exc()),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def clear_clause_functions(master_json, flow, node_id, current_clause_id=None):  # claer caching functions
    try:
        node_path = f'/{flow}/nodes/{node_id}/data/query'
        clauses = extract_sub_json(node_path + '/clauses', master_json)[3]
        for clause_idx, clause in enumerate(clauses):
            try:
                clause_type = clauses[clause_idx]['type']
                clause_id = clauses[clause_idx]['id']
                if current_clause_id and current_clause_id != clause_id:
                    continue
                if clause_type == 'select':
                    Query.select_clause.delete(flow, node_id, clause_id, clause_idx)
                elif clause_type == 'groupBy':
                    Query.group_by_clause.delete(flow, node_id, clause_id, clause_idx)
                elif clause_type == 'orderBy':
                    Query.order_by_clause.delete(flow, node_id, clause_id, clause_idx)
                elif clause_type == 'where':
                    Query.where_clause.delete(flow, node_id, clause_id, clause_idx)
                elif clause_type == 'join':
                    Query.join_clause.delete(flow, node_id, clause_id, clause_idx)
                elif clause_type == 'union':
                    Query.union_clause.delete(flow, node_id, clause_id, clause_idx)
            except Exception as ex:
                message = 'Exception occurred while executing clause'
                unify_printer(level=UNIFY_ERROR, message=message,error=ex, traceback=traceback.format_exc())
                return JsonResponse(internal_server_response(message, traceback=traceback.format_exc()),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as ex:
        message = 'Exception occurred in clear clause function in cache'
        unify_printer(level=UNIFY_ERROR, message=message,
                          error=ex, traceback=traceback.format_exc())
        return JsonResponse(internal_server_response(message, traceback=traceback.format_exc()),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def clear_node_functions(master_json, flow_name, links, node_id, include_this_node_id=False):  # claer caching functions
    try:
        descendants = []
        if include_this_node_id:
            descendants = [node_id]
        find_descendants(master_json, flow_name, links, node_id, descendants)
        for node_id in descendants:
            nodeType = master_json[flow_name]['nodes'][node_id]['data']['type']
            if nodeType == 'outputNode':
                continue
            nodes = {"sourceNode": source_node, "joinNode": join_node, "unionNode": union_node}
            # clear_clause_functions(master_json,flow_name, node_id)
            nodes[nodeType].delete(flow_name, node_id)
    except Exception as ex:
        message = 'Exception occurred in clear node function in cache'
        unify_printer(level=UNIFY_ERROR, message=message,
                          error=ex, traceback=traceback.format_exc())
        return JsonResponse(internal_server_response(message, traceback=traceback.format_exc()),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def delete_node(payload_data, flow_name, master_json):
    try:
        node_id = [n_id for n_id in payload_data['deleteNodes'] if not n_id.endswith('-link')]
        links = [l for l in payload_data['deleteNodes'] if l.endswith('-link')]
        # for nid in node_id:
        #     clear_node_functions(master_json, flow_name, links, nid, True)
        for link_id in links:
            source_id = master_json[flow_name]['nodes'][link_id]['source']
            target_id = master_json[flow_name]['nodes'][link_id]['target']
            if node_id in [source_id,target_id]:
                delete_nl(links, link_id, flow_name, master_json)  # This function Delete the Links
        for nid in node_id:
            del master_json[flow_name]['nodes'][nid]
    except Exception as ex:
        message = 'Exception occurred  while delete nodes'
        unify_printer(level=UNIFY_ERROR, message=message,
                          error=ex, traceback=traceback.format_exc())
        return JsonResponse(internal_server_response(message, traceback=traceback.format_exc()),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def delete_nl(links, link_id, flow_name, master_json):
    try:
        source_id = master_json[flow_name]['nodes'][link_id]['source']
        target_id = master_json[flow_name]['nodes'][link_id]['target']
        # clear_node_functions(master_json, flow_name, links, target_id, True)
        del master_json[flow_name]['nodes'][source_id]['data']['children'][target_id]
        del master_json[flow_name]['nodes'][target_id]['data']['parents'][source_id]
        del master_json[flow_name]['nodes'][link_id]
    except Exception as ex:
        message = 'Exception occurred  while delete link'
        unify_printer(level=UNIFY_ERROR, message=message,
                          error=ex, traceback=traceback.format_exc())
        return JsonResponse(internal_server_response(message, traceback=traceback.format_exc()),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def get_source_node(flow, node_id, master_json):
    try:
        for _, param in master_json[flow].get('nodes').get(node_id).get('data').get('parents').items():
            if isinstance(param, dict):
                datainstance_id = param.get('id')
                instance_id = param.get('instanceId')
        return instance_id, datainstance_id
    except Exception as ex:
        message = 'Exception occurred  while get_source_node'
        unify_printer(level=UNIFY_ERROR, message=message,
                          error=ex, traceback=traceback.format_exc())
        return JsonResponse(internal_server_response(message, traceback=traceback.format_exc()),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_col_details(flow, node_id, clause_id=None, parent=False):
    try:
        if node_id.startswith('__tnode__'):
            return JsonResponse(success_response(data=[]), status=status.HTTP_200_OK)
        master_json = get_flow_by_name(flow)
        clause_list = master_json[flow]['nodes'][node_id]['data']['query']['clauses']
        for idx, value in enumerate(clause_list):
            if value['id'] == clause_id:
                break
        qb = Query(master_json, flow, node_id)
        response = qb.get_columns(flow, node_id, idx, parent)
        return JsonResponse(success_response(data=response), status=status.HTTP_200_OK)
    except Exception as ex:
        message = 'Exception occurred  while get_col_details'
        unify_printer(level=UNIFY_ERROR, message=message,
                          error=ex, traceback=traceback.format_exc())
        return JsonResponse(internal_server_response(message, traceback=traceback.format_exc()),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


def process_node(request, flow, node_id):
    try:
        flow_json = get_flow_by_name(flow)
        node_type = get_node_type(flow, node_id, flow_json)
        if node_type.upper() == 'sourceNode'.upper():
            result: DataFrame = source_node(flow, node_id)
        elif node_type.upper() == 'joinNode'.upper():
            result: DataFrame = join_node(flow, node_id)
        elif node_type.upper() == 'unionNode'.upper():
            result: DataFrame = union_node(flow, node_id)
        else:
            response = validation_error_response(invalid_input)
            json_response = JsonResponse(response, status=status.HTTP_200_OK)
            # write_audit(request, response, start, time.time())
            return json_response
        df_json = {}
        df_json['columns'] = list(result.columns)
        if not result.empty:
            queryRange = request.GET.get('range', None)
            if queryRange:
                range = queryRange.split('-')
                start = int(range[0])
                end = int(range[1])
                if start:
                    df_json['counts'] = None
                    # rowCount=None
                else:
                    df_json['counts'] = {'columns': result.shape[1], 'rows': result.shape[0]}
                    # rowCount=result.shape[0]
                result = result.loc[start:end, ~result.columns.duplicated()]
            else:
                result = result.loc[:, ~result.columns.duplicated()]
            df_json['rows'] = json.loads(result.to_json(orient="records", date_format='iso'))
            response = success_response(data=df_json)
        else:
            response = no_content_response()
        json_response = JsonResponse(response, status=status.HTTP_200_OK)
    except Exception as ex:
        message = 'Error occurred while process node.'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return json_response


def process_node_label(request, flow, node_id):
    try:
        start = time.time()
        label = request.data['$literal']
        flow_json = get_flow_by_name(flow)
        if flow_json:
            flow_json[flow]['nodes'][node_id]['data']['label'] = label
        result = update_flow_by_name(flow, flow_json)
        if result:
            response = success_response("Label updated successfully")
        else:
            response = not_accepted_response("No changes found. Label update failed")
        json_response = JsonResponse(response, status=status.HTTP_200_OK)
    except Exception as ex:
        message = 'Exception occurred while update node label'
        unify_printer(level=UNIFY_ERROR, message=message, error=ex,
                      traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # write_audit(request, response, start, time.time())
    return json_response

def get_parent_node_columns(flow, node_id,record,isFileExists=False):
    try:
        node_type = get_node_type(flow, node_id, record)
        if node_type.upper() == 'sourceNode'.upper():
            result: DataFrame = source_node(flow, node_id)
        elif node_type.upper() == 'joinNode'.upper():
            result: DataFrame = join_node(flow, node_id)
        elif node_type.upper() == 'unionNode'.upper():
            result: DataFrame = union_node(flow, node_id)
        columns=result.convert_dtypes().dtypes
        columnMapping=[]
        slno=1
        if isFileExists:
            pass
        else:
            for column,d_type  in columns.items():
                doc={"id":slno,"fColumn":{"name":column,"type":str(d_type)},"tColumn":{"name":column,"type":str(d_type)}}
                columnMapping.append(doc)
                slno=slno+1
        return columnMapping
    except Exception as ex:
        message = 'Error occurred while getting parent node columns.'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return json_response

def get_df_from_node(flow_json,flow, node_id):
    try:
        node_type = get_node_type(flow, node_id, flow_json)
        if node_type.upper() == 'sourceNode'.upper():
            result: DataFrame = source_node(flow, node_id)
        elif node_type.upper() == 'joinNode'.upper():
            result: DataFrame = join_node(flow, node_id)
        elif node_type.upper() == 'unionNode'.upper():
            result: DataFrame = union_node(flow, node_id)
        return result
    except Exception as ex:
        message = 'Error occurred while getting data from parent nodes.'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return json_response
    