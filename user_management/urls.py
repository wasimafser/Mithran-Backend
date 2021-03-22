from django.urls import path

from .api import UserAPI

app_name = 'user_management'
urlpatterns = [
    path('user/', UserAPI.as_view(), name='user_api'),
]
