from django.urls import include, path
from .views import *

urlpatterns = [
    path('payments/', PaymentListView.as_view(), name='payment_list'),
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/<int:course_id>/auto-create-payment/',
         AutoCreatePaymentView.as_view(), name='auto-create-payment'),
    path('subjects/', SubjectListView.as_view(), name='subject-list'),
    path('subject/<int:subject_id>/',
         SubjectCourseDetailView.as_view(), name='subject-course-detail'),
]
