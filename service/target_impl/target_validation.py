import os 

from django.http import JsonResponse
from rest_framework import status

from service.files.filevalidate import get_sheetnames_xlsx
from service.util.unify_response import success_response

def file_exists_check (filepath):
        return os.path.isfile (filepath)
    
def get_target_xlsheets(filepath):
    doc={}
    if file_exists_check(filepath):
        sheet_names=get_sheetnames_xlsx(filepath)
        sheet_names.append('New Sheet')
        doc['sheetNames']=sheet_names
    else:
        msg="file Not Exists"
        sheet_names=['New Sheet']
        doc['sheetNames']=sheet_names
    return doc






