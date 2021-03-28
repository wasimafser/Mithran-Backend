from django.urls import path

from .api import *

app_name = 'service'
urlpatterns = [
    path('filter/', ServiceFilterAPI.as_view(), name='service_filter_api'),
    path('type/', ServiceTypeAPI.as_view(), name='service_type_api'),
    path('status/', ServiceStatusAPI.as_view(), name='service_status_api'),
    path('api/', ServiceAPI.as_view(), name='service_api'),
]
