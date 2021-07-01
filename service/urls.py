from django.urls import path

from .api import *

app_name = 'service'
urlpatterns = [
    path('filter/', ServiceFilterAPI.as_view(), name='service_filter_api'),
    path('type/', ServiceTypeAPI.as_view(), name='service_type_api'),
    path('status/', ServiceStatusAPI.as_view(), name='service_status_api'),
    path('api/', ServiceAPI.as_view(), name='service_api'),
    path('state/', ServiceStateAPI.as_view(), name='service_state_api'),
    path('feedback/<int:service_id>/', ServiceFeedbackAPI.as_view(), name='service_feedback_api'),
    path('reports/', ServiceReportAPI.as_view(), name='service_reports_api'),
    path('reports/user/<int:user_id>/', ServiceUserReportAPI.as_view(), name='service_user_reports_api'),
]
