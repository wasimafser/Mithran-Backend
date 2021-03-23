from django.urls import path

from .api import UserAPI
from .views import AuthToken

app_name = 'user_management'
urlpatterns = [
    path('user/', UserAPI.as_view(), name='user_api'),
    path('api-token-auth/', AuthToken.as_view(), name='api-token-auth')
]
