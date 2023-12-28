from django.urls import include, path
from .views import *

urlpatterns = [
    path('payments/', PaymentListView.as_view(), name='payment_list'),
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('course/<int:pk>', CourseDetailView.as_view(), name='course-detail'),
    path('subjects/', SubjectListView.as_view(), name='subject-list'),
    path('subject/<str:name>/',
         SubjectCourseDetailView.as_view(), name='subject-course-detail'),
]
