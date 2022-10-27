from django.urls import path
from user.controller import login, signup, signout

urlpatterns = [
    path("login/", login),
    path("signup/", signup),
    path("signout/", signout),
]
