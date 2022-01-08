import datetime
import traceback

import jwt
from pymongo.errors import ServerSelectionTimeoutError

from service.util.unify_logger import unify_printer, UNIFY_ERROR
from unificater.settings import SECRET_KEY, ALGORITHM, JWT_AGE
from users.user_db_untils import get_user_mongod_connection


def generate_token(name):
    now = datetime.datetime.utcnow()
    payload = {
        'id': name,  # Issued for
        'exp': now + datetime.timedelta(seconds=JWT_AGE),  # Expiration AT
        # 'nbf': now + datetime.timedelta(seconds=JWT_AGE - 10),
        'iat': now  # Issued AT
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    if not isinstance(token, str):
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM).decode('utf-8')
    unify_printer(message=f"Token generated for the USER: {name}")
    return token


def verify_token(token):
    try:
        is_valid = False
        payload = jwt.decode(token, SECRET_KEY, algorithm=ALGORITHM)
        unify_printer(message=f"Payload: {payload}")
        is_valid = True
    except Exception as ex:
        unify_printer(level=UNIFY_ERROR, message='Exception occurred while verify token', error=ex,
                      traceback=traceback.format_exc())
    return is_valid


def get_token_user(token):
    user_name = None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm=ALGORITHM)
        user_name = payload.get('id')
        unify_printer(message=f"Token User: {user_name}")
    except Exception as ex:
        unify_printer(level=UNIFY_ERROR, message='Exception occurred while get token user', error=ex,
                      traceback=traceback.format_exc())
    return user_name


def store_token(user_name, token):
    try:
        # uname = user_name.upper()
        # cache.set(token, uname, JWT_CACHE_AGE)
        # cache.set(uname, token, JWT_CACHE_AGE)
        mongod = get_user_mongod_connection()
        mongod.tokenMgmt.update({"name": user_name}, {"$set": {"token": token, "createdOn": datetime.datetime.now()}},
                                upsert=True)
    except Exception as ex:
        unify_printer(level=UNIFY_ERROR, message='Exception occurred while store token', error=ex,
                      traceback=traceback.format_exc())


def get_token(token):
    status = 'FALSE'
    try:
        mongod = get_user_mongod_connection()
        if mongod:
            cache_dtl = mongod.tokenMgmt.find_one({"token": token})
            # token_name = cache.get(cache_key)
            if cache_dtl:
                token_name = cache_dtl['name']
                status = 'TRUE'
                # cache_token = cache.get(token_name.upper())
                # status = verify_cache_token(cache_key, cache_token)
                from users.user_impl import get_userid_by_name
                get_userid_by_name(token_name)
        else:
            status = 'Technical issue while create connection. Try again later.'
    except Exception as ex:
        status = 'Technical issue while create connection. Try again later.'
        unify_printer(level=UNIFY_ERROR, message='Exception occurred while get token', error=ex,
                      traceback=traceback.format_exc())
    return status


def verify_cache_token(token, cache_token):
    status = False
    if token == cache_token:
        status = True
    return status


def delete_token(token):
    try:
        mongod = get_user_mongod_connection()
        mongod.tokenMgmt.update({"token": token}, {"$set": {"token": None, "modifiedOn": datetime.datetime.now()}})
        # token_name = cache.get(token)
        # cache.delete(token_name)
        # cache.delete(token)
    except Exception as ex:
        unify_printer(level=UNIFY_ERROR, message='Exception occurred while delete token', error=ex,
                      traceback=traceback.format_exc())
