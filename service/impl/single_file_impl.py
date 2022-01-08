import json

import requests
from django.http import JsonResponse
from rest_framework import status

from service.util.http_constances import success_msg
from service.util.unify_response import success_response


def get_restapi_data(request):
    api_url = request.data.get('url', '')
    try:
        if api_url:
            url_data = requests.get(api_url)
            if url_data.headers['content-type'] == 'application/json':
                data = json.loads(url_data.content)
            else:
                data = {'error': 'Requesting data is not Json Type, application not acceppt other Than Json',
                        'contentType ': url_data.headers['content-type']}
    except Exception as ex:
        raise
    return JsonResponse(success_response(message=success_msg, data=data), status=status.HTTP_200_OK)
