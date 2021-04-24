from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from user_management.models import Profile, WorkerSpecialization

from .models import Service, ServiceStatus
from .serializers import *


class ServiceAPI(APIView):

    def post(self, request, format=None):
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            service_data = serializer.initial_data
            # ASSIGN WORKER
            requested_by = Profile.objects.get(id=service_data['requested_by']['id'])
            try:
                all_workers = Profile.objects.filter(
                    user__type='worker',
                    organization=requested_by.organization,
                    specializations=service_data['type']
                )
            except Exception as e:
                print(e)
                return Response({'error': "error"}, status=status.HTTP_400_BAD_REQUEST)
            if all_workers.count() == 0:
                return Response({'error': "No Service Person found for the given task type."}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(
                assigned_to = all_workers.first(),
                requested_by = requested_by
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceFilterAPI(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'type', 'requested_by', 'assigned_to']
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


class ServiceStateAPI(APIView):

    def get(self, request, format=None):
        service_id = request.query_params.get('service_id', None)
        service_state = ServiceState.objects.get(service__id=service_id)
        serializer = ServiceStateSerializer(service_state)
        return Response(serializer.data)

    def put(self, request, format=None):
        service_state = ServiceState.objects.get(service=request.data['service'])
        serializer = ServiceStateSerializer(service_state, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
