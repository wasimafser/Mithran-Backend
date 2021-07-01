from rest_framework import serializers

from .models import *


class VisitorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Visitor
        fields = '__all__'
