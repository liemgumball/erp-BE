from django.urls import include, path
from .views import *

urlpatterns = [
    path('vnpay/', include('vnpay.api_urls')),
    path('payment/', payment.as_view(), name='payment'),
    path('payment_return/', payment_return, name='payment_return')

]
