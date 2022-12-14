import enum
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from order.service import OrderManagementService, PaymentService
from order.serializers import OrderCreateReqSchema, PayReqSchema
from decorators.execption_handler import execption_hanlder
from decorators.auth_handler import must_be_user
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from product.serilaizers import OrderUpdateSchema
from provider.auth_provider import auth_provider

from rest_framework.views import APIView
from decorators.auth_handler import must_be_admin, must_be_user

payment_service = PaymentService()
order_management_service = OrderManagementService()


@method_decorator(csrf_exempt)
@execption_hanlder()
@must_be_user()
@parser_classes([JSONParser])
def pay(request):
    # TODO: 결제요청한 유저id validation
    params = PayReqSchema(data=json.loads(request.body))
    params.is_valid(raise_exception=True)
    return JsonResponse(payment_service.pay(**params.data))


@method_decorator(csrf_exempt)
@must_be_user()
@execption_hanlder()
@parser_classes([JSONParser])
def find_payment(request):
    user_id = request.user["id"]
    return JsonResponse(payment_service.find(user_id), safe=False)


class PaymentAPI(APIView):
    def get(self, request):
        return find_payment(request)

    def post(self, request):
        return pay(request)


@api_view(["GET"])
@execption_hanlder()
@must_be_user()
@parser_classes([JSONParser])
def get_payment(request, payment_id: str):
    auth_token = auth_provider.get_token_from_request(request)
    return JsonResponse(payment_service.get(int(payment_id), request.user["id"], auth_token))


@api_view(["POST"])
@execption_hanlder()
@must_be_user()
@parser_classes([JSONParser])
def order_create(request):

    params = OrderCreateReqSchema(data=request.data)
    params.is_valid(raise_exception=True)
    user_id = request.user["id"]

    created_order = order_management_service._create_order(user_id=user_id, **params.data)

    return JsonResponse(created_order)


@api_view(["GET"])
@execption_hanlder()
@must_be_user()
@parser_classes([JSONParser])
def order_details(request, order_id: int):
    return JsonResponse(order_management_service._get_order_detail(order_id))


@api_view(["PUT"])
@execption_hanlder()
@must_be_admin()
@parser_classes([JSONParser])
def order_status_update(request):
    params = OrderUpdateSchema(data=request.data)
    params.is_valid(raise_exception=True)
    order_id = params.data["order_id"]
    status = params.data["status"]

    a = params.data
    return JsonResponse(order_management_service._deilvery_status_update(order_id, status))
