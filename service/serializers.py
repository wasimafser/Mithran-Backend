from rest_framework import serializers
from user_management.models import (Organization, Profile, User,
                                    WorkerSpecialization)

from .models import *


class ServiceSerializer(serializers.ModelSerializer):
    class ProfileCompact(serializers.ModelSerializer):
        class UserComapact(serializers.ModelSerializer):
            class Meta:
                model = User
                fields = ['full_name']

        user = UserComapact()
        class Meta:
            model = Profile
            fields = ['user', 'contact_number', 'door_number', 'address']

    assigned_to = ProfileCompact(read_only=True)
    requested_by = ProfileCompact(read_only=True)
    # status = serializers.SlugRelatedField(queryset=ServiceStatus.objects.all(), slug_field='name')
    class Meta:
        model = Service
        fields = '__all__'


class ServiceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkerSpecialization
        fields = '__all__'


class ServiceStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceStatus
        fields = '__all__'


class ServiceStateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceState
        fields = '__all__'
