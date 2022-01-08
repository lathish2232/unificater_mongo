import traceback
from datetime import datetime

from django.http import JsonResponse
from rest_framework import status
from service.util.unify_response import internal_server_response

from pymongo import MongoClient
from pymongo import ReturnDocument
from pymongo.results import UpdateResult

from service.util.unify_logger import UNIFY_ERROR, unify_printer
from unificater.settings import DATABASE, DB_HOST, DB_PORT, IS_AUTH_ENABLE, AUTH_DB, AUTH_DB_USER, AUTH_DB_PASS
from users.UserDetails import UserDetails

FLOW_DB = DATABASE

def get_mongod_connection(db=FLOW_DB):
    client = None
    try:
        if not UserDetails.FLOW_MONGO_CONNECTION:
            unify_printer(message='Creating FLow MongoDB client connection')
            CONN_STR = f'mongodb://{DB_HOST}:{DB_PORT}'
            DATABASE_NAME = db
            client = MongoClient(CONN_STR)
            if IS_AUTH_ENABLE:
                client[AUTH_DB].authenticate(AUTH_DB_USER, AUTH_DB_PASS)
            UserDetails.FLOW_MONGO_CONNECTION = client[DATABASE_NAME]
    except Exception as ex:
        message = 'Exception occurred while connection Mongo database'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if client:
            client.close()
        return json_response
    finally:
        if client:
            unify_printer(message='Flow MongoDB client connection closed')
            client.close()
    return UserDetails.FLOW_MONGO_CONNECTION



def extract_sub_json(url, json_str):
    try:
        sub_json = json_str
        level = ""
        json_path = []
        start = 1
        if url.startswith("http"):
            start = 3

        for level in url.split("/")[start:]:
            is_match = False
            if isinstance(sub_json, list):
                for i, sub_json_str in enumerate(sub_json):
                    if sub_json_str.get("id") == level:
                        is_match = True
                        sub_json = sub_json_str
                        json_path.append(i)
                        break
                if not is_match:
                    return "", json_path, level, {}
            elif isinstance(sub_json, dict):
                sub_json = sub_json.get(level)
                json_path.append(level)
        mongodb_path = ""  # '.'.join(json_path)
        return mongodb_path, json_path, level, sub_json
    except Exception as ex:
        message = 'Exception occurred while extract sub json'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return json_response


def insert_json_items(j, keys, newkeyidx, value):
    try:
        for key in keys[:-1]:
            if isinstance(key, str):
                j = j.setdefault(key, {})
            else:
                j = j[key]
        if isinstance(j[keys[-1]], dict):
            j[keys[-1]][newkeyidx] = value
        elif isinstance(j[keys[-1]], list):
            if isinstance(newkeyidx, str):
                raise Exception("Sorry, " + str(newkeyidx) + " is not a number")
            j[keys[-1]].insert(newkeyidx, value)
        else:
            pass
            # raise Exception("Sorry, " + str(keys[-1]) + " is neither Dictionary
    except Exception as ex:
        message = 'Exception occurred while insert_json_items'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return json_response


def update_json_items(j, keys, value):
    try:
        for key in keys[:-1]:
            if isinstance(key, str):
                j = j.setdefault(key, {})
            else:
                j = j[key]
        j[keys[-1]] = value
    except Exception as ex:
        message = 'Exception occurred while  update_json_items'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return json_response


def parse_meta_data_search_input(input):
    try:
        condition = ""
        for con in input:
            op = ""
            if con.get("disable"):
                continue
            if con["isnot"]:
                condition += "~"
            if con["groupOf"] is not None:
                condition += f'({parse_meta_data_search_input(con["groupOf"])})'
            if con["conditionalOperator"] is not None:
                op = " " + con["conditionalOperator"] + " "
            if con["condition"] is not None:
                # if con['condition']["LHS"].upper() != 'DATABASE':
                #     db = con["condition"]["RHS"]
                # else:
                condition += f'{con["condition"]["LHS"].upper()} {con["condition"]["operator"]} lower({con["condition"]["RHS"]}) {op} '
        return condition
    except Exception as ex:
        message = 'Exception occurred  while parse meta data search input'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return json_response
    


def get_meta_data_database(input):
    try:
        db = None
        for con in input:
            op = ""
            if con.get("disable"):
                continue
            if con["condition"] is not None:
                if con['condition']["LHS"].upper() == 'DATABASE':
                    db = con["condition"]["RHS"]
                    break
        return db
    except Exception as ex:
        message = 'Exception occurred  while get_meta_data_database'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return json_response

def get_flow_by_name(flow):
    try:
        mongod = get_mongod_connection(FLOW_DB)
        result = mongod['flows'].find_one({"flowName": flow,"userId": int(UserDetails.LOGGED_IN_USER_ID)}, {"_id":0})
        return result
    except Exception as ex:
        message = 'Exception occurred  while getting flow json from metada database'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return json_response


def get_flowid_by_name(flow):
    try:
        mongod = get_mongod_connection(FLOW_DB)
        result = mongod['flows'].find_one({'flowName': flow}, {'UFID': 1})
        return result
    except Exception as ex:
        message = 'Exception occurred  while get_flowid_by_name'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return json_response
    

def update_flow_by_name(flow_name, flow_json):
    data = None
    try:
        mongod = get_mongod_connection()
        flow_json['modifiedOn'] = datetime.now()
        flow_json['modifiedBy'] = UserDetails.LOGGED_IN_USER_NAME
        # result: UpdateResult = mongod['flows'].update_one({'flowName': flow_name}, {'$set': flow_json})
        result = mongod['flows'].find_one_and_update({'flowName': flow_name}, {'$set': flow_json},return_document=ReturnDocument.AFTER)
        if result:
            data = result[flow_name]
        return data
    except Exception as ex:
        message = 'Exception occurred  while update_flow_by_name'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return json_response
    


def insert_recent_connection(mongod, record):
    try:
        del record['id']
        mongod.recentConnections.update_one({"displayName": record['displayName']}, {"$set": record}, upsert=True)
    except Exception as ex:
        message = 'Exception occurred  while update_flow_by_name'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return json_response


def update_recent_connection(mongod, record, data):
    try:
        mongod.recentConnections.update(record, {"$set": data}, upsert=True)
    except Exception as ex:
        message = 'Exception occurred  while update_flow_by_name'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return json_response


def get_node_type(flow, node_id, flow_json):
    try:
        node = flow_json.get(flow).get('nodes').get(node_id)
        if node:
            node_type = node.get('data').get('type')
        else:
            raise Exception(f'Node \'{node_id}\' not exist.')
        return node_type
    except Exception as ex:
        message = 'Exception occurred  while update_flow_by_name'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return json_response


def is_not_null_or_empty(data):
    try:
        is_valid = False
        if data and len(data) > 0:
            is_valid = True
        return is_valid
    except Exception as ex:
        message = 'Exception occurred  while update_flow_by_name'
        unify_printer(level=UNIFY_ERROR, message=message,
                      error=ex, traceback=traceback.format_exc())
        response = internal_server_response(message, traceback.format_exc())
        json_response = JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return json_response
