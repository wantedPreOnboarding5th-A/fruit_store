from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from order.service import OrderManagementService, PaymentService
from order.serializers import OrderCreateReqSchema, PayReqSchema
from decorators.execption_handler import execption_hanlder
<<<<<<< Updated upstream
=======
from decorators.auth_handler import must_be_admin, must_be_user
>>>>>>> Stashed changes

payment_service = PaymentService()
order_management_service = OrderManagementService()


@api_view(["POST"])
@execption_hanlder()
@parser_classes([JSONParser])
def pay(request):
    params = PayReqSchema(data=request.data)
    params.is_valid(raise_exception=True)
    return JsonResponse(payment_service.pay(**params.data))


@must_be_user()
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
    params = request.get("status")
    return JsonResponse(order_management_service._get_order(params))


@must_be_admin()
@api_view(["PUT"])
@execption_hanlder()
@parser_classes([JSONParser])
def order_status_update(request):
    # enum 체크 구현하기
    order_id = request.order_id
    params = request.status
    return JsonResponse(order_management_service._deilvery_status_update(order_id, params))
