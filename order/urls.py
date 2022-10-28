from django.urls import path
from order.controller import order_create, order_details, order_status_update, pay

urlpatterns = [
    path("payments/", pay),
    path("orders/create", order_create),
    path("orders/details/<int:order_id>", order_details),
    path("orders/status", order_status_update),
]
