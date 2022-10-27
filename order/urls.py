from django.urls import path
from order.controller import pay

urlpatterns = [
    path("payments/", pay),
]
