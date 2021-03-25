from rest_framework import serializers

from .models import User

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=False)
    password = serializers.CharField(read_only=True)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)

        if user.last_name:
            user.full_name = f"{user.first_name} {user.last_name}"
        else:
            user.full_name = f"{user.first_name}"

        user.set_password("mithran@123")
        user.save()

        return user

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'full_name',
            'email',
            'password'
        )
