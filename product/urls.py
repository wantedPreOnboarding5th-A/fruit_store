from django.urls import path

from product.controller import get_list, CartAPI, ProcuctAPI

urlpatterns = [
    path("product/", ProcuctAPI.as_view()),
    path("product/<int:product_id>", ProcuctAPI.as_view()),
    path("product/list", get_list),
    path("carts/", CartAPI.as_view()),
]
