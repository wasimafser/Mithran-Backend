from rest_framework import serializers

from .models import Service
from user_management.models import Worker, User, WorkerSpecialization


class ServiceSerializer(serializers.ModelSerializer):
    class WorkerCompact(serializers.ModelSerializer):
        class UserComapact(serializers.ModelSerializer):
            class Meta:
                model = User
                fields = ['full_name']

        user = UserComapact()
        class Meta:
            model = Worker
            fields = ['user', 'contact_number']

    assigned_to = WorkerCompact(read_only=True)
    class Meta:
        model = Service
        fields = '__all__'


class ServiceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkerSpecialization
        fields = '__all__'
