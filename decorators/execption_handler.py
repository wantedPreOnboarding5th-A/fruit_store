from functools import wraps
from exceptions import CustomBaseExecption
from django.http import JsonResponse
from rest_framework import status


def execption_hanlder():
    def decorator(api_func):
        @wraps(api_func)
        def _wrapped_view(request, *args, **kwargs):
            try:
                return api_func(request, *args, **kwargs)
            except Exception as e:
                err_msg = e.msg if isinstance(e, CustomBaseExecption) else e.args[0]
                err_status = (
                    e.status if hasattr(e, "status") else status.HTTP_400_BAD_REQUEST
                )
                return JsonResponse(data={"msg": err_msg}, status=err_status)

        return _wrapped_view

    return decorator
