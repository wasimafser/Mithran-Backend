from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, AllowAny

from .serializers import UserSerializer, ConsumerSerializer
from .models import User, Worker, Consumer

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
        user_type = request.data.pop('type', None)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            print(user)
            if user_type == 'worker':
                Worker.objects.create(user=user)
            else:
                Consumer.objects.create(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganizationAPI(APIView):

    def get(self, request, format=None):
        print(request.data)
        return Response({"test": "test"})


class ConsumerAPI(APIView):

    def get(self, request, format=None):
        user_id = request.query_params.get('user_id', None)
        consumer = Consumer.objects.get(user__id=user_id)
        serializer = ConsumerSerializer(consumer)
        return Response(serializer.data)

    def put(self, request, format=None):
        consumer = Consumer.objects.get(id=request.data['id'])
        serializer = ConsumerSerializer(consumer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
