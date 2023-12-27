from rest_framework import serializers
from .models import *


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'phone', 'name', 'enroll_number']

    def create(self, validated_data):
        client = CustomUser.objects.create_user(**validated_data)
        return client


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ['is_superuser', 'groups',
                   'user_permissions', 'is_active', 'password']
