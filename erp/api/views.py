from datetime import datetime
from rest_framework import generics, status, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import *
from .serializers import *


class PaymentListView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.AllowAny]
    serializer_class = PaymentSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('student_name_like', openapi.IN_QUERY,
                              description="Search query", type=openapi.TYPE_STRING),
            openapi.Parameter('_sort', openapi.IN_QUERY,
                              description="Sort field", type=openapi.TYPE_STRING),
            openapi.Parameter('_order', openapi.IN_QUERY,
                              description="Sort order", type=openapi.TYPE_STRING),
        ],
        responses={
            200: openapi.Response(description="OK", schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
            400: openapi.Response(description="Bad Request"),
            401: openapi.Response(description="Unauthorized"),
        },
        operation_description="Your operation description here."
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        payments = Payment.objects.all()

        search_query = self.request.query_params.get('student_name_like', None)
        sort_by = self.request.query_params.get('_sort', 'id')
        order = self.request.query_params.get('_order', 'asc')

        if search_query:
            payments = payments.filter(student__name__icontains=search_query)

        if sort_by:
            allowed_fields = [
                field.name for field in Payment._meta.get_fields()]
            if sort_by in allowed_fields:
                order_by_field = sort_by if order == 'asc' else f'-{sort_by}'
                payments = payments.order_by(order_by_field)

        return payments


class AutoCreatePaymentView(generics.CreateAPIView):
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        course_id = self.kwargs.get('course_id')
        course = Course.objects.get(pk=course_id)
        students = course.students.all()

        # Default amount or use the provided amount
        amount = request.data.get('amount', 100)

        payments_to_create = []

        for student in students:
            start_date = datetime.now()
            end_date = start_date + timedelta(weeks=4)

            payment_data = {
                'student': student,
                'course': course,
                'start_date': start_date,
                'end_date': end_date,
                'amount': amount,
            }

            payments_to_create.append(payment_data)

        # Create payments in bulk
        Payment.objects.bulk_create([Payment(**data)
                                    for data in payments_to_create])

        return Response({'message': 'Payments created successfully.'}, status=status.HTTP_201_CREATED)


class CourseListView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.AllowAny]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class SubjectListView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.AllowAny]
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectCourseDetailView(generics.RetrieveAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.AllowAny]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def retrieve(self, request, *args, **kwargs):
        name = self.kwargs.get('name')
        try:
            subject = Subject.objects.get(name=name)
        except Subject.DoesNotExist:
            return Response({'error': 'Subject not found'}, status=status.HTTP_404_NOT_FOUND)

        courses = Course.objects.filter(subject=subject)
        serializer = self.get_serializer(courses, many=True)

        return Response({'name': subject.name, 'courses': serializer.data})


class CourseDetailView(generics.RetrieveAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.AllowAny]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def retrieve(self, request, *args, **kwargs):
        course_id = self.kwargs.get('pk')
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        return super().retrieve(request, *args, **kwargs)
        return Response({'subject': subject.name, 'courses': serializer.data})


class CourseCreateView(generics.CreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        # Extract subject data from the request
        subject_name = request.data.get('subject')

        # Check if the subject name is provided
        if subject_name:
            # Check if the subject already exists
            subject_instance, created = Subject.objects.get_or_create(
                name=subject_name)
        else:
            # Handle the case where subject name is not provided
            subject_instance = None
            created = False  # Set created to False

        # Update request data with the subject instance
        request.data['subject'] = subject_instance.id if subject_instance else None

        # Use the CourseSerializer to validate and create the course
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SubjectListCreateAPIView(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.AllowAny]
