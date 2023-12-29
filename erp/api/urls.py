from django.urls import include, path
from .views import *

urlpatterns = [
    path('payments/', PaymentListView.as_view(), name='payment_list'),
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('reports/', ReportListView.as_view(), name='report-list'),
    path('report/', ReportCreateView.as_view(), name='report-create'),
    path('course/<int:pk>', CourseDetailView.as_view(), name='course-detail'),
    path('courses/<int:course_id>/auto-create-payment/',
         AutoCreatePaymentView.as_view(), name='auto-create-payment'),
    path('subjects/', SubjectListView.as_view(), name='subject-list'),
    path('subject/<str:name>/',
         SubjectCourseDetailView.as_view(), name='subject-course-detail'),
    path('courses/add/', CourseCreateView.as_view(), name='course-create'),
    path('subjects/add/', SubjectListCreateAPIView.as_view(),
         name='subject-list-create'),
    path('enroll-course/', EnrollCourseView.as_view(), name='enroll-course'),
]
