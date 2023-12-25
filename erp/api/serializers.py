from rest_framework import serializers
from .models import *
from custom_users.models import *


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    student = StudentSerializer()

    class Meta:
        model = Payment
        fields = '__all__'
