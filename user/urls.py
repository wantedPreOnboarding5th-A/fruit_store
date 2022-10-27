from django.urls import path
from user.controller import login, signup

urlpatterns = [
    path("login/", login),
    path("signup/", signup),
]
