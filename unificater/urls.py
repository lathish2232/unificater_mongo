"""unificater URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path

# testing funcions
from service.views import __operators, get_logs_by_flow, get_logs_by_request, node_output  # _functions
from service.views import baron_tree
from service.views import connection_properties, node_label
from service.views import parent_col_detail
from service.views import expression_builder
from service.views import function_list
from service.views import get_connection_type, get_database_params, flow, \
    get_flows, get_pattern_connections
from service.views import get_folder_structure, node_counter, get_fullflow
from service.views import instances, instance_by_id, exc_data_instance
from service.views import meta_search, recentconnections, execute_query, data_instances, data_instance_by_id, \
    extract_file_data, get_db_schema
from service.views import nodes, get_targets, target_subType_and_params, target_data_instances
from service.views import target_instance, target_columns, run_target

admin.site.site_header = "Unificater Admin"

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Unificater API Document",
        default_version='v1',
        description="api reference",
        terms_of_service="https://www.unificater.com/policies/terms/",
        contact=openapi.Contact(email="lathish2232@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('flow', flow),
    path('flows', get_flows),
    path('getFolderStructure', get_folder_structure),
    path('recentconnections', recentconnections),
    path('connectionTypes', get_connection_type),
    path('targetTypes', get_targets),
    path('barontree', baron_tree),
    path('operators', __operators),
    path('functions', function_list),
    path('<str:flow>/nodes', nodes),
    path('<str:flow>/instances', instances),
    path('<str:flow>/nodecounter', node_counter),
    path('<str:flow>/recentconnections', recentconnections),
    path('connectionTypes/<str:type>', connection_properties),
    path('connectionTypes/database/<str:db_name>', get_database_params),
    path('connectionTypes/pattern/<str:pattern_type>', get_pattern_connections),
    path('<str:flow>/instances/<str:instance_id>', instance_by_id),
    path('<str:flow>/targets/<str:node_id>', target_instance),
    path('<str:flow>/instances/<str:instance_id>/query', execute_query),
    path('<str:flow>/instances/<str:instance_id>/database', get_db_schema),
    path('<str:flow>/instances/<str:instance_id>/metasearch', meta_search),
    path('<str:flow>/instances/<str:instance_id>/dataInstances', data_instances),
    path('<str:flow>/instances/<str:instance_id>/targetdatainstances', target_data_instances),
    path('<str:flow>/instances/<str:instance_id>/dataInstances/<str:data_instance_id>', data_instance_by_id),
    path('<str:flow>/instances/<str:instance_id>/dataInstances/<str:data_instance_id>/extractdata', extract_file_data),
    path('<str:flow>/instances/<str:instance_id>/dataInstances/<str:data_instance_id>/exc', exc_data_instance),
    path('<str:flow>/nodes/<str:node_id>/data/label', node_label),
    path('<str:flow>/nodes/<str:node_id>/<str:clause_id>/coldetail', parent_col_detail),
    path('targetTypes/<str:target_type>', target_subType_and_params),
    path('<str:flow>/targets/<str:node_id>/tColumns', target_columns),
    path('<str:flow>/targets/<str:node_id>/executeTragets', run_target),
    path('<str:flow>/nodes/<str:node_id>/output', node_output),
    path('<str:flow>/nodes/<str:node_id>/<str:clause_id>/parentcoldetail', parent_col_detail),
    path('<str:flow>/<str:node_id>/<str:clause_id>/<str:column_id>/expression', expression_builder),
    path('<str:flow>/<str:node_id>/<str:clause_id>/<str:column_id>/methods', expression_builder),
    path('log/flow/<str:flow>', get_logs_by_flow),
    path('log/request/<str:reqid>', get_logs_by_request),
    path('<str:flow>', get_fullflow),
    path('admin/', admin.site.urls),
    path('user/', include('users.urls')),
    url(r'.*', include(('service.urls', "service"), namespace="service"))

]

handler404 = 'service.util.exception.error_404'
handler500 = 'service.util.exception.error_500'
