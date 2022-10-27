from functools import wraps
from exceptions import CustomBaseExecption
from django.http import JsonResponse
from rest_framework import status
from provider.auth_provider import auth_provider
from exceptions import NotAuthorizedError


def must_be_user():
    def decorator(api_func):
        @wraps(api_func)
        def _wrapped_view(request, *args, **kwargs):
            auth_token = request.META.get("HTTP_AUTHORIZATION", None)
            if auth_token == None:
                raise NotAuthorizedError
            user = auth_provider.check_auth(auth_token)
            request.user = user
            return api_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


def must_be_admin():
    def decorator(api_func):
        @wraps(api_func)
        def _wrapped_view(request, *args, **kwargs):
            auth_token = request.META.get("HTTP_AUTHORIZATION", None)
            if auth_token == None:
                raise NotAuthorizedError
            user = auth_provider.check_is_admin(auth_token)
            request.user = user
            return api_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
