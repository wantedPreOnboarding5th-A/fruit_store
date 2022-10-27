from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from order.service import PaymentService
from order.serializers import PayReqSchema
from decorators.execption_handler import execption_hanlder
from decorators.auth_handler import must_be_user

payment_service = PaymentService()


@api_view(["POST"])
@execption_hanlder()
@parser_classes([JSONParser])
@must_be_user()
def pay(request):
    params = PayReqSchema(data=request.data)
    params.is_valid(raise_exception=True)
    return JsonResponse(payment_service.pay(**params.data))
