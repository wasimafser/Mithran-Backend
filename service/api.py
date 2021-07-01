from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from user_management.models import Profile, User, WorkerSpecialization, Organization

from .models import Service, ServiceStatus
from .serializers import *

import datetime


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


class ServiceReportAPI(APIView):

    def get(self, request, format=None):
        workers = User.objects.filter(profile__organization__id=1, type='worker')
        data = []
        for worker in workers:
            _data = {
                'user_id': worker.id,
                'full_name': worker.full_name,
                'total_services': 0,
                'total_work_time': datetime.timedelta(0, 0, 0),
            }
            for serivce in Service.objects.filter(assigned_to__user=worker):
                _data['total_services'] += 1
                if serivce.total_work_time:
                    _data['total_work_time'] += serivce.total_work_time

            data.append(_data)

        return Response(data)


class ServiceFeedbackAPI(generics.ListCreateAPIView):
    queryset = ServiceFeedback.objects.all()
    serializer_class = ServiceFeedbackSerializer

    def get_queryset(self):
        service_id = self.kwargs['service_id']
        return ServiceFeedback.objects.filter(service__id=service_id)


class ServiceUserReportAPI(APIView):

    def get(self, request, user_id, format=None):
        services = Service.objects.filter(assigned_to__user__id=user_id)
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)

