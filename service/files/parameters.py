import os
import traceback

from django.http import JsonResponse
from rest_framework import status

from service.files.filevalidate import Filevalidate, get_sheetnames_xlsx, update_sheet_name
from service.util.db_utils import get_data_from_dataSource
from service.util.unify_logger import unify_printer, UNIFY_ERROR
from service.util.unify_response import success_response, validation_error_response, not_accepted_response
from service.util.unify_uris import CONN_TYPE_ID

file_validate = Filevalidate()


def get_file_params(request,type):
    try:
        fileType=request.data['fileType']
        unify_printer(message=f'file parameters of {fileType}')
        doc = {'type': None, 'displayName': None, 'fileType': None,
               'dataInstances': [
                   {'id': 'dataInstances_1', 'functionName': None, 'name':None,'isFwf': None, 'isActiveInFlow': False,
                    'dataParameters': None}]}
        
        doc['fileType'] = fileType
        doc['type'] = type
        doc['displayName'] = None
        if fileType in['csv','xlsx']:
            if fileType=='xlsx':
                fileType='excel'
            url = '/connectionJson/connectionTypes/' + CONN_TYPE_ID.get(
                type) + '/connections/' + fileType
            result = get_data_from_dataSource('dataSource', url)
            if result:
                doc['dataInstances'][0]['functionName'] = result['functionName']
                doc['dataInstances'][0]['isFwf'] = result['isFwf']
                doc['dataInstances'][0]['dataParameters'] = result['connectionParameters']
            response=doc
        else:
            response= not_accepted_response(f"Instance type {fileType} is not supported.")
    except Exception as ex:
        unify_printer(level=UNIFY_ERROR, message='Exception occurred while getting file parameters',
                      error=ex, traceback=traceback.format_exc())
        raise Exception(ex)
    return response


def validate_file(filepath,fileType):
    err_msg = None
    # if not file_validate.file_exists_check(filepath):
    #     err_msg = "File is not exists in this path,please give correct file path details"
    # elif not file_validate.non_empty_file_check(filepath):
    #     err_msg = f"File is empty,please give correct non empty file... Empty File path is:-{filepath}"
    # elif not file_validate.file_extension_check(filepath):
    #     err_msg = "Supported file extensions excel,csv,txt only"
    # elif not file_validate.check_file_type(filepath,fileType):
    #     err_msg="File type and file formate are  diffrent.please Select correct type and formate"
    if not err_msg:
        err_msg = "successful"
    return err_msg


def file_params(request, type):
    filepath = request.data['file']
    filetype = os.path.basename(filepath).split('.')[-1]
    doc = {'type': None, 'displayName': None, 'fileType': None, 'dataInstances': []}
    validatefile = validate_file(filepath)
    if validatefile == 'successful':
        doc['type'] = type
        doc['fileType'] = filetype
        doc['displayName'] = os.path.basename(filepath)
        if filetype == 'csv':
            url = '/connectionJson/connectionTypes/' + CONN_TYPE_ID.get(
                type) + '/connections/' + filetype.upper()
            result = get_data_from_dataSource('dataSource', url)
            if result:
                rec = {'id': 'dataInstances_1', 'functionName': result['functionName'], 'isFwf': result['isFwf'],
                       'dataParameters': result['connectionParameters']}
                doc['dataInstances'].append(rec)
                for rec in doc['dataInstances'][0]['dataParameters']:
                    if rec['fieldName'] == "filepath_or_buffer":
                        rec['userValue'] = filepath

        elif filetype == 'xlsx':
            url = '/connectionJson/connectionTypes/' + CONN_TYPE_ID.get(
                type) + '/connections/' + 'excel'
            result = get_data_from_dataSource('dataSource', url)
            if result:
                sheetNames = get_sheetnames_xlsx(filepath)
                rec = {'id': None, 'functionName': result['functionName'], 'isFwf': result['isFwf'],
                       'dataParameters': result['connectionParameters']}
                data_ins = []
                for i, name in enumerate(sheetNames):
                    data_ins.append(update_sheet_name(result, rec, name, i, filepath).copy())
                doc['dataInstances'] = data_ins
        elif filetype == 'json':
            url = '/connectionJson/connectionTypes/' + CONN_TYPE_ID.get(
                type) + '/connections/' + 'json'
            result = get_data_from_dataSource('dataSource', url)
            if result:
                rec = {'id': 'dataInstance_1', 'functionName': result['functionName'], 'isFwf': result['isFwf'],
                       'dataParameters': result['connectionParameters']}
                doc['dataInstances'].append(rec)
                for rec in doc['dataInstances'][0]['dataParameters']:
                    if rec['fieldName'] == "path_or_buf":
                        rec['userValue'] = filepath
        return JsonResponse(success_response(data=doc), status=status.HTTP_200_OK)
    else:
        return JsonResponse(validation_error_response(message=validatefile), status=status.HTTP_200_OK)


def validate_csv_parametars(dataInstances):
    args = {}
    for item in dataInstances:
        # args ={dataparam["fieldName"]: dataparam["userValue"] for dataparam in item.get('dataParameters') if dataparam["userValue"] != None and dataparam["userValue"]!=''}
        args = {dataparam["fieldName"]: dataparam["userValue"] for dataparam in item.get('dataParameters') if
                dataparam["userValue"] != dataparam['parameterDefaultValue']}
    for key in args:
        if args[key].isdigit():
            args[key] = int(args[key])
