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
        subject_id = self.kwargs.get('subject_id')
        try:
            subject = Subject.objects.get(pk=subject_id)
        except Subject.DoesNotExist:
            return Response({'error': 'Subject not found'}, status=status.HTTP_404_NOT_FOUND)

        courses = Course.objects.filter(subject=subject)
        serializer = self.get_serializer(courses, many=True)

        return Response({'subject': subject.name, 'courses': serializer.data})
