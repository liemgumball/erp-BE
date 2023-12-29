from rest_framework import serializers
from .models import *
from custom_users.serializers import UserSerializer


class SubjectSerializer(serializers.ModelSerializer):
    course_length = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = ['id', 'name', 'course_length']

    def get_course_length(self, subject):
        return Course.objects.filter(subject=subject).count()


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


class ReportSerializer(serializers.ModelSerializer):
    student = UserSerializer()

    class Meta:
        model = Report
        fields = '__all__'


class ReportWriteOnlyStudentSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all())

    class Meta:
        model = Report
        fields = '__all__'
