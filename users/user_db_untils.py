import traceback
from time import sleep

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

from service.util.unify_logger import unify_printer, UNIFY_ERROR
from unificater.settings import DB_HOST, DB_PORT, IS_AUTH_ENABLE, AUTH_DB, AUTH_DB_USER, AUTH_DB_PASS, DATABASE
from users.UserDetails import UserDetails

FLOW_DB = DATABASE


def get_user_mongod_connection(db=FLOW_DB):
    client = None
    loop = 1
    sleep_time = 15
    try:
        if UserDetails.MONGO_CONNECTION is None:
            unify_printer(message='Creating User MongoDB client connection')
            CONN_STR = f'mongodb://{DB_HOST}:{DB_PORT}'
            DATABASE_NAME = db
            while True:
                client = MongoClient(CONN_STR)
                if IS_AUTH_ENABLE:
                    client[AUTH_DB].authenticate(AUTH_DB_USER, AUTH_DB_PASS)
                UserDetails.MONGO_CONNECTION = client[DATABASE_NAME]
                if UserDetails.MONGO_CONNECTION or loop > 3:
                    break
                else:
                    unify_printer(message=f"Not able to create users db connections, trying again after {sleep_time} Sec")
                    sleep(sleep_time)
                    loop = loop + 1
    except ServerSelectionTimeoutError as ex:
        unify_printer(level=UNIFY_ERROR, message='Not able to create users db connections', error=ex,
                      traceback=traceback.format_exc())
        raise Exception(ex)
    except Exception as ex:
        unify_printer(level=UNIFY_ERROR, message='Exception occurred while connection User Mongo database', error=ex,
                      traceback=traceback.format_exc())
        raise Exception(ex)

    finally:
        if client:
            unify_printer(message='User MongoDB client connection closed')
            client.close()
    return UserDetails.MONGO_CONNECTION
