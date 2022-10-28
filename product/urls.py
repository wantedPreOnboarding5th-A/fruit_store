from django.urls import path

from product.controller import ProcuctAPI, get_list

urlpatterns = [
    path("product/", ProcuctAPI.as_view()),
    path("product/<int:product_id>", ProcuctAPI.as_view()),
    path("product/list", get_list),
]
