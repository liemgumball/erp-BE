from rest_framework import serializers
from .models import *
from custom_users.serializers import UserSerializer


class PaymentSerializer(serializers.ModelSerializer):
    student = UserSerializer()

    class Meta:
        model = Payment
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
