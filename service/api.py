from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, filters
from rest_framework.permissions import IsAdminUser, AllowAny

from .serializers import ServiceSerializer, ServiceTypeSerializer
from .models import Service
from user_management.models import WorkerSpecialization


class ServiceAPI(APIView):

    def post(self, request, format=None):
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceFilterAPI(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filterset_fields = ['status', 'type']
    search_fields = ['id',]


class ServiceTypeAPI(APIView):
    def get(self, request, format=None):
        specializations = WorkerSpecialization.objects.all()
        serializer = ServiceTypeSerializer(specializations, many=True)
        return Response(serializer.data)
