from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import *

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



