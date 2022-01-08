import traceback

from service.util.db_utils import get_data_from_dataSource
from service.util.unify_logger import unify_printer, UNIFY_ERROR
from service.util.unify_uris import CONN_TYPE_ID


def get_databases(type):
    try:
        unify_printer(message='Getting databases')
        url_str = '/connectionJson/connectionTypes/' + CONN_TYPE_ID[type] + '/connections'
        result = get_data_from_dataSource('dataSource', url_str)
        if result:
            for element in result:
                del element['functionName']
                del element['isFwf']
                del element['returnType']
                del element['connectionParameters']
    except Exception as ex:
        unify_printer(level=UNIFY_ERROR, message='Exception occurred while getting databases',
                      error=ex, traceback=traceback.format_exc())
        raise Exception(ex)
    return result
