from rest_framework import serializers

from .models import User, Consumer, Worker, Organization

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=False)
    id = serializers.IntegerField(read_only=True)
    # password = serializers.CharField(read_only=True)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)

        if user.last_name:
            user.full_name = f"{user.first_name} {user.last_name}"
        else:
            user.full_name = f"{user.first_name}"

        password = validated_data.get('password', None)
        if password:
            user.set_password(password)
        else:
            user.set_password("mithran@123")
        user.save()

        return user

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'password'
        )


class ConsumerSerializer(serializers.ModelSerializer):
    organization = serializers.SlugRelatedField(queryset=Organization.objects.all(), slug_field='code')

    class Meta:
        model = Consumer
        fields = '__all__'
