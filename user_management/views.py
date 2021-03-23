from django.shortcuts import render

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import UserSerializer

# Create your views here.

class AuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        try:
            user = User.objects.get(email=email)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                user_serialized = UserSerializer(user)
                return Response({
                    'user': user_serialized.data,
                    'token': token.key
                })
            return Response(
                {'error': 'No such user found'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print(e)
            return Response({'error': "error"})
