from django.urls import path
from .views import *

urlpatterns = [
    path('payments/', PaymentListView.as_view(), name='payment_list'),
    path('courses/', CourseListView.as_view(), name='course-list'),
]
