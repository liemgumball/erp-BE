from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import *
from drf_yasg import openapi

# Create your views here.


class UserRegistration(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class UserLogin(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(
                request=request, email=email, password=password)

            if user:
                token, created = Token.objects.get_or_create(user=user)
                user = CustomUser.objects.get(email=email)
                return Response({'accessToken': token.key, 'user': {
                    'id': user.id,
                    'role': 'admin' if user.is_staff else 'student',
                    'name': user.name,
                    'email': user.email
                }})
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

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
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = CustomUser.objects.filter(is_staff=False)
        search_query = self.request.query_params.get('name_like', None)
        sort_by = self.request.query_params.get('_sort', 'id')
        order = self.request.query_params.get('_order', 'asc')

        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        if sort_by:
            allowed_fields = [
                field.name for field in CustomUser._meta.get_fields()]
            if sort_by in allowed_fields:
                order_by_field = sort_by if order == 'asc' else f'-{sort_by}'
                queryset = queryset.order_by(order_by_field)

        return queryset


class UserUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    def get_object(self):
        user_id = self.kwargs.get('pk')
        return self.queryset.get(pk=user_id)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Customize the response data
        user_data = {
            'id': instance.id,
            'name': instance.name,
            'email': instance.email,
            'role': 'admin' if instance.is_staff else 'student',
        }

        return Response({'user': user_data}, status=status.HTTP_200_OK)
