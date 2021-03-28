from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, filters
from rest_framework.permissions import IsAdminUser, AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import *
from .models import Service, ServiceStatus
from user_management.models import WorkerSpecialization, Worker


class ServiceAPI(APIView):

    def post(self, request, format=None):
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            service_data = serializer.validated_data
            # ASSIGN WORKER
            try:
                all_workers = Worker.objects.filter(
                    organization=service_data['requested_by'].organization,
                    specializations=service_data['type']
                )
            except Exception as e:
                print(e)
                return Response({'error': "error"}, status=status.HTTP_400_BAD_REQUEST)
            if all_workers.count() == 0:
                return Response({'error': "No Service Person found for the given task type."}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(assigned_to = all_workers.first())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceFilterAPI(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'type', 'requested_by']
    # search_fields = ['id',]


class ServiceTypeAPI(APIView):
    def get(self, request, format=None):
        specializations = WorkerSpecialization.objects.all()
        serializer = ServiceTypeSerializer(specializations, many=True)
        return Response(serializer.data)


class ServiceStatusAPI(APIView):
    def get(self, request, format=None):
        statuss = ServiceStatus.objects.all()
        serializer = ServiceStatusSerializer(statuss, many=True)
        return Response(serializer.data)
