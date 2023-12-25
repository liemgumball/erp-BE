from django.urls import path
from .views import *

urlpatterns = [
    path('payments/', payment_list, name='payment_list'),
]
