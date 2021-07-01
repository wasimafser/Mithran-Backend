from django.urls import path

from .api import *
from .views import AuthToken

app_name = 'user_management'
urlpatterns = [
    path('user/', UserAPI.as_view(), name='user_api'),
    path('user/filter/', UserFilterAPI.as_view(), name='user_filter_api'),
    path('profile/', ProfileAPI.as_view(), name='consumer_api'),
    path('api-token-auth/', AuthToken.as_view(), name='api-token-auth'),
]
