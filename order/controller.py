from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from order.service import OrderManagementService, PaymentService
from order.serializers import OrderCreateReqSchema, OrderGetReqSchema, PayReqSchema
from decorators.execption_handler import execption_hanlder
from decorators.auth_handler import must_be_user

payment_service = PaymentService()

order_management_service = OrderManagementService()


@api_view(["POST"])
@execption_hanlder()
@parser_classes([JSONParser])
@must_be_user()
def pay(request):
    params = PayReqSchema(data=request.data)
    params.is_valid(raise_exception=True)
    return JsonResponse(payment_service.pay(**params.data))


@api_view(["POST"])
@execption_hanlder()
@parser_classes([JSONParser])
def order_create(request):
    params = OrderCreateReqSchema(data=request.data)
    params.is_valid(raise_exception=True)
    return JsonResponse(order_management_service._create_order(params))


@api_view(["GET"])
@execption_hanlder()
@parser_classes([JSONParser])
def order_details(request):
    params = OrderGetReqSchema(data=request.data)
    params.is_valid(raise_exception=True)
    return JsonResponse(order_management_service._get_order(params))
