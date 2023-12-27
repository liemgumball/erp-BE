from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('students', StudentListView.as_view(), name='student-list'),
    path('<int:pk>/', UserUpdateView.as_view(), name='user-update'),
]
