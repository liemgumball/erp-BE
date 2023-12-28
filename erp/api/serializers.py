from rest_framework import serializers
from .models import *
from custom_users.serializers import UserSerializer


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    student = UserSerializer()
    course = CourseSerializer()

    class Meta:
        model = Payment
        fields = '__all__'
