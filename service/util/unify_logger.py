import json
import logging
import time
import traceback
from datetime import datetime

from bson.objectid import ObjectId
from django.http import JsonResponse
from pymongo import MongoClient
from rest_framework import status

from service.util.unify_response import success_response, internal_server_response, no_content_response
from unificater.settings import IS_AUTH_ENABLE, AUTH_DB, AUTH_DB_USER, AUTH_DB_PASS, DB_HOST, DB_PORT, DATABASE
from users.UserDetails import UserDetails

LOGGER_NAME = 'unify_service'
AUDIT_LOGGER_NAME = 'AUDIT'
LOGGER = logging.getLogger(LOGGER_NAME)

UNIFY_DEBUG = 'DEBUG'
UNIFY_INFO = 'INFO'
UNIFY_ERROR = 'ERROR'

LOGGER_MESSAGE = ''
LOGGER_ERROR = None
LOGGER_TRACEBACK = None
LOGGER_FILE = None
LOGGER_API = 'MAIN'

unify_log_list = []


def unify_printer(level=UNIFY_INFO, message=LOGGER_MESSAGE, error=LOGGER_ERROR,
                  traceback=LOGGER_TRACEBACK, location=None):
    if not UserDetails.REQUEST_API:
        api = LOGGER_API
    else:
        api = UserDetails.REQUEST_API

    if error and not isinstance(error, str):
        error = str(error)

    msg_list = [message, error, traceback, location]
    msg = ' | '.join(item for item in msg_list if item)
    msg = f'[API: {api}] ' + msg

    if level.upper() == 'DEBUG':
        LOGGER.debug(msg)
    elif level.upper() == 'INFO':
        LOGGER.info(msg)
    elif level.upper() == 'ERROR':
        LOGGER.error(msg)
    else:
        LOGGER.info(msg)
    unify_log(level=level, message=message, error=error, traceback=traceback, name=LOGGER_NAME, location=location)


def unify_audit_printer(request, response: JsonResponse, starts, ends):
    start_dt = datetime.fromtimestamp(starts).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    end_dt = datetime.fromtimestamp(ends).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    elapsed = round((ends - starts) / 1000, 3)
    client_host = request.META.get('REMOTE_ADDR')
    response = json.loads(response.getvalue().decode())
    message = f'[{AUDIT_LOGGER_NAME}] {UserDetails.LOGGED_IN_USER_ID} | {client_host} | {request.path} | {request.method} | {start_dt} | {end_dt} | {elapsed} | {response.get("code")} | {response.get("message")}'
    LOGGER.info(message)
    message_1 = {
        'requestHost': client_host,
        'requestAPI': request.path,
        'requestMethod': request.method,
        'requestReceivedAt': start_dt,
        'requestEndsAt': end_dt,
        'elapsedTime': elapsed,
        'responseCode': response.get("code"),
        'responseMessage': response.get("message")
    }
    unify_log(level=UNIFY_INFO, message=message_1, error=None, traceback=None, name=AUDIT_LOGGER_NAME)


def unify_log(level=UNIFY_INFO, message=LOGGER_MESSAGE, error=LOGGER_ERROR, traceback=LOGGER_TRACEBACK,
              name=LOGGER_NAME, location=None):
    now = time.time()
    logId = f'{now}_{round(UserDetails.LOGGED_IN_USER_ID)}'
    log_msg = {
        '_id': str(ObjectId()),
        'correlationId': UserDetails.CORRELATION_ID,
        'userId': UserDetails.LOGGED_IN_USER_ID,
        'flowId': None,
        'flowName': UserDetails.FLOW,
        'endpoint': UserDetails.REQUEST_API,
        'level': level,
        'name': name,
        'message': message,
        'error': error,
        'traceback': traceback,
        'location': location,
        'timestamp': now
    }
    unify_log_list.append(log_msg)


def insert_unify_log():
    try:
        # log_db = get_logs_mongod_connection()
        if unify_log_list:
            # log_db['unifyLogs'].insert_many(unify_log_list, ordered=False)
            unify_log_list.clear()
        else:
            pass
    except Exception as ex:
        LOGGER.error(f"Error occurred while insert: {str(traceback.format_exc())}")
    return unify_log_list


def get_logs_by_flowname(flow):
    try:
        log_db = get_logs_mongod_connection()
        result = log_db['unifyLogs'].find({'flowName': flow})
        if result:
            json_response = JsonResponse(success_response(data=list(result)), status=status.HTTP_200_OK)
        else:
            json_response = JsonResponse(no_content_response(), status=status.HTTP_200_OK)
    except Exception as ex:
        message = 'Error occurred while get logs'
        unify_printer(level=UNIFY_ERROR, message=message, error=ex, traceback=traceback.format_exc())
        json_response = JsonResponse(internal_server_response(message, traceback.format_exc()),
                                     status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return json_response


def get_logs_by_request_id(reqId):
    try:
        log_db = get_logs_mongod_connection()
        result = log_db['unifyLogs'].find({'correlationId': reqId})
        if result:
            json_response = JsonResponse(success_response(data=list(result)), status=status.HTTP_200_OK)
        else:
            json_response = JsonResponse(no_content_response(), status=status.HTTP_200_OK)
    except Exception as ex:
        message = 'Error occurred while get logs'
        unify_printer(level=UNIFY_ERROR, message=message, error=ex, traceback=traceback.format_exc())
        json_response = JsonResponse(internal_server_response(message, traceback.format_exc()),
                                     status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return json_response


FLOW_DB = DATABASE


def get_logs_mongod_connection(db=FLOW_DB):
    client = None
    try:
        if not UserDetails.FLOW_MONGO_CONNECTION:
            CONN_STR = f'mongodb://{DB_HOST}:{DB_PORT}'
            DATABASE_NAME = db
            client = MongoClient(CONN_STR)
            if IS_AUTH_ENABLE:
                client[AUTH_DB].authenticate(AUTH_DB_USER, AUTH_DB_PASS)
            UserDetails.FLOW_MONGO_CONNECTION = client[DATABASE_NAME]
    except Exception as ex:
        raise Exception(ex)
    finally:
        if client:
            client.close()
    return UserDetails.FLOW_MONGO_CONNECTION
