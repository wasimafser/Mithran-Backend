from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser, AllowAny

from .serializers import UserSerializer, ProfileSerializer
from .models import User, Profile, Profile

class UserAPI(APIView):
    """
    API to create a user or get all users.
    """
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            Profile.objects.create(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganizationAPI(APIView):

    def get(self, request, format=None):
        print(request.data)
        return Response({"test": "test"})


class ProfileAPI(APIView):

    def get(self, request, format=None):
        user_id = request.query_params.get('user_id', None)
        consumer = Profile.objects.get(user__id=user_id)
        serializer = ProfileSerializer(consumer)
        return Response(serializer.data)

    def put(self, request, format=None):
        consumer = Profile.objects.get(id=request.data['id'])
        serializer = ProfileSerializer(consumer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserFilterAPI(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['profile__organization', 'type']
    search_fields = ['full_name']
