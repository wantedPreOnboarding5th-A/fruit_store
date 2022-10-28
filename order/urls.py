from django.urls import path
from order.controller import PaymentAPI, get_payment

urlpatterns = [
    path("payments/", PaymentAPI.as_view()),
    path("payments/<payment_id>", get_payment),
]
