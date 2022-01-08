
from service.util.unify_uris import TARGET_TYPE_ID
from service.util.db_utils import get_data_from_targetTypes

db_list=[
    {
        "id": "dbId_1",
        "name": "postgreSql",
        "displayName": "PostgreSQL"
    },
    {
        "id": "dbId_2",
        "name": "mysql",
        "displayName": "MySQL"
    }
]
def get_databaseTypes():
    return db_list


def get_file_params(target_type,fileType):
    url = f'/targetTypes/{TARGET_TYPE_ID[target_type]}/connections/{fileType}'
    target_data = get_data_from_targetTypes('targetTypes', url)
    doc = {'id': None,
            "type": "file",
            'functionName': None,
            'displayName': None,
            "fileType": fileType,
            "nodeId": None,
            'isActiveInFlow': False,
            "isFileExists": False,
            'dataParameters': None
                                }
    if target_data:
        doc['dataParameters'] = target_data['targetParameters']
        doc['functionName'] = target_data['functionName']
    target_data = doc
    return target_data

def get_db_params(request,target_type):
    dbtype=request.data['name']
    url = f'/targetTypes/{TARGET_TYPE_ID[target_type]}/connections' 
    target_data = get_data_from_targetTypes('targetTypes', url)
    for rec in target_data:
        if rec['name']==dbtype:
            doc = {'id': None,
                    "type": target_type,
                    'functionName':None,
                    'displayName': None,
                    "dbType": dbtype,
                    "nodeId": None,
                    'isActiveInFlow': False,
                    "isTableExists": False,
                    'dataParameters': rec['connectionParameters']
                                        }
    return doc