from django.urls import path

from product.controller import create, delete, get_detail, get_list, CartAPI

urlpatterns = [
    path("register/", create),
    path("list/", get_list),
    path("detail/", get_detail),
    path("delete/", delete),
    path("carts/", CartAPI.as_view()),
]