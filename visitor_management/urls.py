from django.urls import path

from .api import *

app_name = 'visitor_management'
urlpatterns = [
    path('filter/', VisitorFilterAPI.as_view(), name='visitor_filter_api'),
    path('api/', VisitorAPI.as_view(), name='visitor_api')
]
