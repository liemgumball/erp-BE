from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import *
from .serializers import *


class PaymentListView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]
    serializer_class = PaymentSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('name_like', openapi.IN_QUERY,
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
    def get_queryset(self):
        payments = Payment.objects.all()

        search_query = self.request.query_params.get('name_like', None)
        sort_by = self.request.query_params.get('_sort', 'id')
        order = self.request.query_params.get('_order', 'asc')

        if search_query:
            payments = payments.filter(name__icontains=search_query)

        if sort_by:
            allowed_fields = [
                field.name for field in Payment._meta.get_fields()]
            if sort_by in allowed_fields:
                order_by_field = sort_by if order == 'asc' else f'-{sort_by}'
                payments = payments.order_by(order_by_field)

        return payments


class CourseListView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
