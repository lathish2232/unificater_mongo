from django.conf.urls import url
from django.urls import path

from service.views import process_request, execute_query

urlpatterns = [
    # path('validate/query', query_validation),
    path('', process_request),

]
